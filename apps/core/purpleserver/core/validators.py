import re
import logging
import requests
import phonenumbers
from constance import config
from datetime import datetime
from rest_framework import serializers
from purplship.core import units, utils
from purpleserver.core import dataunits, datatypes

logger = logging.getLogger(__name__)
DIMENSIONS = ['width', 'height', 'length', 'dimension_unit']


def dimensions_required_together(value):
    any_dimension_specified = any(value.get(dim) is not None for dim in DIMENSIONS)
    has_any_dimension_undefined = any(value.get(dim) is None for dim in DIMENSIONS)

    if any_dimension_specified and has_any_dimension_undefined:
        raise serializers.ValidationError(
            'When one dimension is specified, all must be specified with a dimension_unit'
        )


def valid_time_format(value):

    try:
        datetime.strptime(value, '%H:%M')
    except Exception:
        raise serializers.ValidationError(
            'The time format must match HH:HM'
        )


def valid_date_format(value):

    try:
        datetime.strptime(value, '%Y-%m-%d')
    except Exception:
        raise serializers.ValidationError(
            'The date format must match YYYY-MM-DD'
        )


def valid_datetime_format(value):

    try:
        datetime.strptime(value, '%Y-%m-%d')
    except Exception:
        raise serializers.ValidationError(
            'The datetime format must match YYYY-MM-DD HH:HM'
        )


class PresetSerializer:

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        if data is not None and 'package_preset' in data:
            preset = next(
                (presets[data['package_preset']] for carrier, presets in dataunits.REFERENCE_MODELS["package_presets"].items() if data['package_preset'] in presets),
                {}
            )

            kwargs.update(data={
                **data,
                "width": data.get("width", preset.get("width")),
                "length": data.get("length", preset.get("length")),
                "height": data.get("height", preset.get("height")),
                "dimension_unit": data.get("dimension_unit", preset.get("dimension_unit"))
            })

        super().__init__(*args, **kwargs)


class AugmentedAddressSerializer:

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        if data is not None:

            # Format and validate Postal Code
            if all(data.get(key) is not None for key in ['country_code', 'postal_code']):
                postal_code = data['postal_code']
                country_code = data['country_code']

                if country_code == units.Country.CA.name:
                    formatted = ''.join([c for c in postal_code.split() if c not in ['-', '_']]).upper()
                    if not re.match(r'^([A-Za-z]\d[A-Za-z][-]?\d[A-Za-z]\d)', formatted):
                        raise serializers.ValidationError('The Canadian postal code must match Z9Z9Z9')

                elif country_code == units.Country.US.name:
                    formatted = ''.join(postal_code.split())
                    if not re.match(r'^\d{5}(-\d{4})?$', formatted):
                        raise serializers.ValidationError('The American postal code must match 9999 or 99999')

                else:
                    formatted = postal_code

                data.update({**data, 'postal_code': formatted})

            # Format and validate Phone Number
            if all(data.get(key) is not None and data.get(key) != "" for key in ['country_code', 'phone_number']):
                phone_number = data['phone_number']
                country_code = data['country_code']

                try:
                    formatted = phonenumbers.parse(phone_number, country_code)
                    data.update({**data, 'phone_number': phonenumbers.format_number(formatted, phonenumbers.PhoneNumberFormat.INTERNATIONAL)})
                except Exception as e:
                    logger.warning(e)
                    raise serializers.ValidationError("Invalid phone number format")

            kwargs.update(data=data)

        super().__init__(*args, **kwargs)


class GoogleGeocode:
    @staticmethod
    def get_url() -> str:
        return "https://maps.googleapis.com/maps/api/geocode/json"

    @staticmethod
    def get_api_key() -> str:
        key = config.GOOGLE_CLOUD_API_KEY

        if key is None or len(key) == 0:
            raise Exception("No GOOGLE_CLOUD_API_KEY provided for address validation")

        return key

    @staticmethod
    def format_address(address: datatypes.Address) -> str:
        address_string = utils.SF.concat_str(
            address.address_line1 or "",
            address.address_line2 or "",
            address.postal_code or "",
            address.city or "",
            join=True
        )

        if address_string is None:
            raise Exception("At least one address info must be provided (address_line1, city and/or postal_code)")

        enriched_address = utils.SF.concat_str(
            address_string,
            address.state_code or "",
            address.country_code or "",
            join=True
        )

        return enriched_address.replace(" ", "+")

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        formatted_address = GoogleGeocode.format_address(address)

        logger.debug(f'sending address validation request to Google Geocode API: {formatted_address}')
        response = requests.request(
            "GET",
            GoogleGeocode.get_url(),
            params=dict(address=formatted_address, key=GoogleGeocode.get_api_key(), location_type="ROOFTOP")
        )
        response_data = response.json()
        success = response_data.get("status") == "OK"
        meta = dict(results=response_data.get("results"))

        return datatypes.AddressValidation(success=success, meta=meta)

