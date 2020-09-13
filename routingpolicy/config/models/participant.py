"""Participant Parameter Configuration Model."""
# Standard Library
from typing import Union

# Third Party
from pydantic import BaseModel, StrictInt, StrictStr, StrictBool, conint, validator

ASN16 = conint(strict=True, ge=1, lt=64512)
ASN32 = conint(strict=True, ge=65536, lt=4200000000)


class Participant(BaseModel):
    """48 IX Participant Parameters."""

    id: StrictInt
    name: StrictStr
    asn: Union[ASN16, ASN32]
    irr: Union[StrictBool, StrictStr]

    @validator("irr")
    def validate_irr(cls, value):
        """Ensure IRR is either false or an IRR object string."""
        if value is True:
            raise ValueError("IRR can only be 'false' or a valid IRR object string.")
