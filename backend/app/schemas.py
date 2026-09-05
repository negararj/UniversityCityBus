from pydantic import BaseModel


class StopOut(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    route: str | None = None

    model_config = {"from_attributes": True}
