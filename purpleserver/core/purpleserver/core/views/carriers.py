import logging
from typing import List
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.router import router
from purpleserver.core.serializers import CarrierSettingsList, CarrierFilters
from purpleserver.core.gateway import get_carriers
from purpleserver.core.datatypes import CarrierSettings

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    methods=['get'],
    tags=['CORE'],
    responses={200: CarrierSettingsList()},
    operation_description=("""
    Return the list of configured carriers
    """),
    operation_id="Carriers",
    query_serializer=CarrierFilters
)
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
def carriers_settings(request: Request):
    try:
        try:
            query = request.query_params
            response: List[CarrierSettings] = get_carriers(
                carrier_type=query.get('carrier'),
                carrier_name=query.get('carrierName'),
                test=query.get('test'),
            )
            carriers = [
                dict(
                    carrier=carrier.carrier,
                    carrier_name=carrier.settings['carrier_name'],
                    test=carrier.settings['test']
                )
                for carrier in response
            ]
            return Response(carriers, status=status.HTTP_200_OK)
        except Exception as pe:
            logger.exception(pe)
            return Response(pe.args, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('carriers', carriers_settings, name='Carriers'))
