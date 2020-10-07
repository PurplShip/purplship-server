from typing import Dict, Type

from rest_framework.serializers import ModelSerializer, Serializer, ChoiceField

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import CARRIERS, PlainDictField
from purpleserver.providers.models import MODELS, Carrier

CarrierName = str
CarrierSerializer = Type[ModelSerializer]


def generate_provider_serializer() -> Dict[CarrierName, CarrierSerializer]:

    def _create_serializer(name) -> CarrierSerializer:
        class _Serializer(ModelSerializer):
            class Meta:
                model = MODELS[name]
                exclude = ['id', 'created_at', 'updated_at', 'user']

        return _Serializer

    return {
        name: _create_serializer(name) for name in MODELS.keys()
    }


SERIALIZERS = generate_provider_serializer()


class CarrierSerializer(Serializer):
    carrier_name = ChoiceField(required=True, choices=CARRIERS, help_text="Indicates a carrier (type)")
    carrier_config = PlainDictField(required=True, help_text="the logistics service provider connection configuration")

    def __init__(self, *args, **kwargs):
        carrier_name: str = kwargs.get('data', {}).get('carrier_name')
        instance, *_ = args + (None, )

        if carrier_name in SERIALIZERS:
            carrier_config_data: dict = kwargs.get('data', {}).get('carrier_config', {})
            serializer = SERIALIZERS[carrier_name]
            _args = (
                [MODELS[carrier_name].objects.get(pk=carrier_config_data['id'])] if "id" in carrier_config_data else []
            )
            carrier_config = SerializerDecorator[serializer](*_args, data=carrier_config_data).data
            kwargs.update(data=dict(carrier_name=carrier_name, carrier_config=carrier_config))

            if "id" in carrier_config_data:
                args = _args

        super().__init__(*args, **kwargs)

    def create(self, validated_data: dict) -> Carrier:
        carrier_name = validated_data['carrier_name']
        carrier_config = {
            **validated_data['carrier_config'],
            "user": validated_data["user"]
        }

        return MODELS[carrier_name].objects.create(**carrier_config)

    def update(self, instance: Carrier, validated_data: dict) -> Carrier:
        carrier_config = validated_data['carrier_config']

        for key, val in carrier_config.items():
            setattr(instance, key, val)

        instance.save()
        return instance
