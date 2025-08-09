import math
import random
from datetime import UTC, datetime

from fastapi import HTTPException, status
from geopy.distance import geodesic
from geopy.point import Point
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.crud.random_problem_crud import RandomProblemCRUD
from app.schema.random_problem import (
    RandomProblemComplete,
    RandomProblemCreate,
    RandomProblemForDB,
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
) -> RandomProblemResponse:
    """Complete a random problem."""
    settings = get_settings()
    crud = RandomProblemCRUD(db)
    problem = crud.read(problem_id)

    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    if problem.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problem is already in '{problem.status}' status.",
        )

    # ユーザーの位置と問題の位置の距離を計算
    user_location = (problem_data.user_latitude, problem_data.user_longitude)
    problem_location = (problem.latitude, problem.longitude)
    distance = geodesic(user_location, problem_location).meters

    # 距離が閾値より大きい場合は、何もせずに現在の問題情報を返す
    if distance > settings.DISTANCE_THRESHOLD_METERS:
        return RandomProblemResponse.model_validate(problem)

    # 距離が閾値内の場合は、問題を更新する
    now = datetime.now(UTC)
    update_data = RandomProblemForDB(
        user_id=problem.user_id,
        longitude=problem.longitude,
        latitude=problem.latitude,
        status="completed",
        completed_at=now,
        ended_at=now,
        image_url=problem_data.image_url,
    )
    updated_problem = crud.update(problem_id, update_data)

    if not updated_problem:
        # このケースは通常発生しないはずだが、念のため
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update the problem.",
        )

    return RandomProblemResponse.model_validate(updated_problem)


def give_up_problem(
    db: Session,
    problem_id: int,
) -> RandomProblemResponse:
    """Give up a random problem."""
    crud = RandomProblemCRUD(db)
    problem = crud.read(problem_id)

    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    if problem.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problem is already in '{problem.status}' status.",
        )

    update_data = RandomProblemForDB(
        user_id=problem.user_id,
        longitude=problem.longitude,
        latitude=problem.latitude,
        status="given_up",
        ended_at=datetime.now(UTC),
    )
    updated_problem = crud.update(problem_id, update_data)

    if not updated_problem:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update the problem.",
        )

    return RandomProblemResponse.model_validate(updated_problem)
