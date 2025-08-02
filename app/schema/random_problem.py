from datetime import datetime

from pydantic import BaseModel


class RandomProblemBase(BaseModel):
    user_id: int


class RandomProblemCreate(RandomProblemBase):
    center_longitude: float
    center_latitude: float
    radius: float


class RandomProblemResponse(RandomProblemBase):
    random_problem_id: int
    longitude: float
    latitude: float
    created_at: datetime
    ended_at: datetime | None = None
    status: str
    image_url: str | None = None


class RandomProblemComplete(RandomProblemBase):
    image_url: str
    user_longitude: float
    user_latitude: float


class RandomProblemGivenUp(RandomProblemBase):
    pass
