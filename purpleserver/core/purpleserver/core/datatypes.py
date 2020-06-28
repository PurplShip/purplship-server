import attr
from typing import List, Dict, Type, TypeVar
from jstruct import JStruct, JList, REQUIRED
from purplship.core.utils import to_dict
from purplship.core.models import (
    Address,
    Doc,
    Payment,
    Customs,
    Parcel,
    RateDetails,
    Parcel,
    Message,
    TrackingDetails,
    TrackingRequest,
    ShipmentDetails,
    ShipmentRequest as BaseShipmentRequest,
    RateRequest,
    Insurance
)


class CarrierSettings:
    def __init__(self, carrier_name: str, carrier_id: str, test: bool = None, **kwargs):
        self.carrier_name = carrier_name
        self.carrier_id = carrier_id
        self.test = test

        for name, value in kwargs.items():
            if name not in ['carrier_ptr']:
                self.__setattr__(name, value)

    def dict(self):
        return {
            name: value for name, value in self.__dict__.items()
            if name not in ['carrier_name']
        }

    @classmethod
    def create(cls, data: object):
        return cls(**to_dict(data))


@attr.s(auto_attribs=True)
class ShipmentRate(RateRequest):
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]

    rates: List[RateDetails] = JList[RateDetails]

    services: List[str] = []
    options: Dict = {}
    reference: str = ""

    carrier_ids: List[str] = []


@attr.s(auto_attribs=True)
class ShipmentRequest(BaseShipmentRequest):
    service: str = JStruct[str, REQUIRED]
    selected_rate_id: str = JStruct[str, REQUIRED]

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]
    rates: List[RateDetails] = JList[RateDetails, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    doc_images: List[Doc] = JList[Doc]

    options: Dict = {}
    reference: str = ""


@attr.s(auto_attribs=True)
class Shipment:
    carrier_id: str
    carrier_name: str
    tracking_number: str
    label: str
    service: str
    selected_rate_id: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]

    selected_rate: RateDetails = JStruct[RateDetails, REQUIRED]
    rates: List[RateDetails] = JList[RateDetails, REQUIRED]

    tracking_url: str = None

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    doc_images: List[Doc] = JList[Doc]

    options: Dict = {}


@attr.s(auto_attribs=True)
class ErrorResponse:
    messages: List[Message] = JList[Message]


@attr.s(auto_attribs=True)
class RateResponse:
    messages: List[Message] = JList[Message]
    rates: List[RateDetails] = JList[RateDetails]


@attr.s(auto_attribs=True)
class ShipmentResponse:
    messages: List[Message] = JList[Message]
    shipment: Shipment = JStruct[Shipment]


@attr.s(auto_attribs=True)
class TrackingResponse:
    messages: List[Message] = JList[Message]
    tracking_details: TrackingDetails = JStruct[TrackingDetails]


@attr.s(auto_attribs=True)
class Error:
    message: str = None
    code: str = None
    details: Dict = None
