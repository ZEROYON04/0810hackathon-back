import math
import random

from geopy.distance import geodesic
from geopy.point import Point
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
    """球上の円の中からランダムに一点を生成し、新しいランダムな問題を作成"""
    center_point = Point(problem_data.center_latitude, problem_data.center_longitude)

    # ランダムな方位角を生成 (0-360度)
    bearing = random.uniform(0, 360)

    # 逆関数サンプリング法を用いて、円内のランダムな距離を生成
    # これにより、円の面積内で均一な点の分布が得られる
    # 半径はkm単位
    random_distance_km = problem_data.radius * math.sqrt(random.random())

    # 中心点から指定した距離と方位角にある新しい点を計算
    destination = geodesic(kilometers=random_distance_km).destination(
        point=center_point,
        bearing=bearing,
    )

    db_problem_data = RandomProblemForDB(
        user_id=problem_data.user_id,
        latitude=destination.latitude,
        longitude=destination.longitude,
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
