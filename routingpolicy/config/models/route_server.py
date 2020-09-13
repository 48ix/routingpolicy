"""Route Server Parameter Configuration Model."""

from pydantic import BaseModel, StrictStr, StrictInt


class RouteServer(BaseModel):
    """48 IX Route Server Parameters."""

    id: StrictInt
    name: StrictStr
    metro_id: StrictInt
    loc_id: StrictInt
