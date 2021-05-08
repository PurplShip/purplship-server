from typing import Optional
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, CharField, ChoiceField, BooleanField

from purplship.core.utils import DP
from purpleserver.core.gateway import Shipments, Carriers
from purpleserver.core.utils import SerializerDecorator, owned_model_serializer, save_one_to_one_data, \
    save_many_to_many_data
import purpleserver.core.datatypes as datatypes
from purpleserver.providers.models import Carrier
from purpleserver.core.serializers import (
    SHIPMENT_STATUS,
    ShipmentStatus,
    ShipmentData,
    Shipment,
    Payment,
    Rate,
    ShippingRequest,
    ShipmentCancelRequest,
    LABEL_TYPES,
    LabelType,
    Message,
)
from purpleserver.manager.serializers.address import AddressSerializer
from purpleserver.manager.serializers.customs import CustomsSerializer
from purpleserver.manager.serializers.parcel import ParcelSerializer
from purpleserver.manager.serializers.rate import RateSerializer
import purpleserver.manager.models as models


@owned_model_serializer
class ShipmentSerializer(ShipmentData):
    status = ChoiceField(required=False, choices=SHIPMENT_STATUS)
    selected_rate_id = CharField(required=False)
    rates = Rate(many=True, required=False)
    label = CharField(required=False, allow_blank=True, allow_null=True)
    tracking_number = CharField(required=False, allow_blank=True, allow_null=True)
    shipment_identifier = CharField(required=False, allow_blank=True, allow_null=True)
    selected_rate = Rate(required=False, allow_null=True)
    tracking_url = CharField(required=False, allow_blank=True, allow_null=True)
    test_mode = BooleanField(required=False)
    messages = Message(many=True, required=False)

    def __init__(self, instance: models.Shipment = None, **kwargs):
        data = kwargs.get('data')

        if data is not None and isinstance(data, str):
            kwargs.update(data=ShipmentData(models.Shipment.objects.get(pk=data)).data)

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Shipment:
        test = validated_data.get('test')
        context_user = self._context_user
        carrier_ids = validated_data.get('carrier_ids', [])
        carriers = Carriers.list(carrier_ids=carrier_ids, created_by=context_user) if any(carrier_ids) else []
        rate_response: datatypes.RateResponse = SerializerDecorator[RateSerializer](
            data=validated_data, context_user=context_user).save(test=test).instance
        test_mode = all([r.test_mode for r in rate_response.rates])

        shipment_data = {
            key: value for key, value in validated_data.items()
            if key in models.Shipment.DIRECT_PROPS and value is not None
        }

        shipment_data.update(
            shipper=save_one_to_one_data(
                'shipper', AddressSerializer, payload=validated_data, context_user=context_user),

            recipient=save_one_to_one_data(
                'recipient', AddressSerializer, payload=validated_data, context_user=context_user),

            customs=save_one_to_one_data(
                'customs', CustomsSerializer, payload=validated_data, context_user=context_user),
        )

        shipment = models.Shipment.objects.create(**{
            **shipment_data,
            'test_mode': test_mode,
            'created_by': context_user,
            'rates': DP.to_dict(rate_response.rates),
            'messages': DP.to_dict(rate_response.messages)
        })
        shipment.carriers.set(carriers)

        save_many_to_many_data(
            'parcels', ParcelSerializer, shipment, payload=validated_data, context_user=self._context_user)

        return shipment

    @transaction.atomic
    def update(self, instance: models.Shipment, validated_data: dict) -> models.Shipment:
        changes = []
        data = validated_data.copy()
        context_user = self._context_user or instance.created_by

        for key, val in data.items():
            if key in models.Shipment.DIRECT_PROPS:
                setattr(instance, key, val)
                changes.append(key)
                validated_data.pop(key)

            if key in models.Shipment.RELATIONAL_PROPS and val is None:
                prop = getattr(instance, key)
                changes.append(key)
                # Delete related data from database if payload set to null
                if hasattr(prop, 'delete'):
                    prop.delete()
                    setattr(instance, key, None)
                    validated_data.pop(key)

        if validated_data.get('customs') is not None:
            changes.append('customs')
            save_one_to_one_data('customs', CustomsSerializer, instance, payload=validated_data, context_user=context_user)

        if 'selected_rate' in validated_data:
            selected_rate = validated_data.get('selected_rate', {})
            carrier = Carrier.objects.filter(carrier_id=selected_rate.get('carrier_id')).first()
            instance.test_mode = selected_rate.get('test_mode', instance.test_mode)

            instance.selected_rate = {**selected_rate, **({'carrier_ref': carrier.id} if carrier is not None else {})}
            instance.selected_rate_carrier = carrier
            changes += ['selected_rate', 'selected_rate_carrier']

        instance.save(update_fields=changes)

        if 'carrier_ids' in validated_data:
            carrier_ids = validated_data.get('carrier_ids', [])
            carriers = Carriers.list(carrier_ids=carrier_ids, created_by=instance.created_by) if any(carrier_ids) else instance.carriers
            instance.carriers.set(carriers)

        return instance


@owned_model_serializer
class ShipmentPurchaseData(Serializer):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
    label_type = ChoiceField(required=False, choices=LABEL_TYPES, default=LabelType.PDF.name, help_text="The shipment label file type.")
    payment = Payment(required=False, help_text="The payment details")


@owned_model_serializer
class ShipmentValidationData(Shipment):
    rates = Rate(many=True, required=True)
    payment = Payment(required=True)

    def create(self, validated_data: dict) -> datatypes.Shipment:
        return Shipments.create(
            ShippingRequest(validated_data).data,
            resolve_tracking_url=(
                lambda shipment: reverse(
                    "purpleserver.manager:shipment-tracker",
                    kwargs=dict(tracking_number=shipment.tracking_number, carrier_name=shipment.carrier_name)
                )
            )
        )


class ShipmentCancelSerializer(Shipment):

    def update(self, instance: models.Shipment, validated_data: dict) -> datatypes.ConfirmationResponse:
        if instance.status == ShipmentStatus.purchased.value:
            response = Shipments.cancel(
                payload=ShipmentCancelRequest(instance).data,
                carrier=instance.selected_rate_carrier
            )
        else:
            response = datatypes.ConfirmationResponse(
                messages=[],
                confirmation=datatypes.Confirmation(
                    carrier_name="None Selected",
                    carrier_id="None Selected",
                    success=True,
                    operation="Cancel Shipment",
                )
            )

        instance.delete()
        return response


def reset_related_shipment_rates(shipment: Optional[models.Shipment]):
    if shipment is not None:
        shipment.selected_rate = None
        shipment.rates = []
        shipment.messages = []
        shipment.save()
