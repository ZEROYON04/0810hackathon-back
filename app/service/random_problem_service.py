import math
import random

from sqlalchemy.orm import Session

from app.crud.random_problem_crud import RandomProblemCRUD
from app.schema.random_problem import (
    RandomProblemComplete,
    RandomProblemCreate,
    RandomProblemForDB,
    RandomProblemGivenUp,
    RandomProblemResponse,
)


def get_problems_by_user_id(db: Session, user_id: int) -> list[RandomProblemResponse]:
    """Get random problems by user_id."""
    crud = RandomProblemCRUD(db)
    problems = crud.read_by_user_id(user_id)
    return [RandomProblemResponse.model_validate(problem) for problem in problems]


def create_random_problem(db: Session, problem_data: RandomProblemCreate) -> RandomProblemResponse:
    """Create a new random problem with a random coordinate within a circle."""
    # 緯度経度1度あたりの距離(km)
    lat_per_km = 111.0
    lon_per_km = 91.0

    # 半径(km)を緯度経度の差に変換
    radius_in_lat = problem_data.radius / lat_per_km
    radius_in_lon = problem_data.radius / lon_per_km

    # 円内のランダムな点を生成
    angle = 2 * math.pi * random.random()
    r = random.random()  # 0-1の範囲で半径の割合をランダムに決定
    latitude = problem_data.center_latitude + r * radius_in_lat * math.cos(angle)
    longitude = problem_data.center_longitude + r * radius_in_lon * math.sin(angle)

    db_problem_data = RandomProblemForDB(
        user_id=problem_data.user_id,
        latitude=latitude,
        longitude=longitude,
    )

    crud = RandomProblemCRUD(db)
    problem = crud.create(db_problem_data)
    return RandomProblemResponse.model_validate(problem)


def complete_problem(
    db: Session,
    problem_id: int,
    problem_data: RandomProblemComplete,
) -> RandomProblemResponse | None:
    """Complete a random problem."""
    crud = RandomProblemCRUD(db)
    problem = crud.update(problem_id, problem_data)
    if problem:
        return RandomProblemResponse.model_validate(problem)
    return None


def give_up_problem(
    db: Session,
    problem_id: int,
    problem_data: RandomProblemGivenUp,
) -> RandomProblemResponse | None:
    """Give up a random problem."""
    crud = RandomProblemCRUD(db)
    problem = crud.update(problem_id, problem_data)
    if problem:
        return RandomProblemResponse.model_validate(problem)
    return None
