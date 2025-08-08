from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.schema.random_problem import (
    RandomProblemComplete,
    RandomProblemCreate,
    RandomProblemGivenUp,
    RandomProblemResponse,
)
from app.service.random_problem_service import (
    complete_problem as complete_problem_service,
)
from app.service.random_problem_service import (
    create_random_problem as create_random_problem_service,
)
from app.service.random_problem_service import (
    get_problems_by_user_id,
)
from app.service.random_problem_service import (
    give_up_problem as give_up_problem_service,
)

settings = get_settings()
logger = settings.configure_logging()

router = APIRouter(prefix="/random-problem", tags=["Random Problem"])


@router.get(
    "/{user_id}",
    summary="ユーザーに紐づいたランダム問題の一覧を取得するAPIエンドポイント。",
    description="ユーザーIDに紐づくランダム問題の情報をデータベースから取得して返します。",
)
async def get_random_problem(
    user_id: Annotated[int, Path(..., description="ID of the user to fetch random problems for")],
    db: Annotated[Session, Depends(get_db)],
) -> list[RandomProblemResponse]:
    logger.info("Fetching random problems for user_id: %s", user_id)
    return get_problems_by_user_id(db, user_id)


@router.post(
    "/create",
    summary="新しいランダム問題を作成するAPIエンドポイント。",
    status_code=status.HTTP_201_CREATED,
    description="""
ユーザーIDと中心座標、半径(km)を指定して、円の中からランダムな座標を持つ新しいランダム問題を作成します。
""",
)
async def create_random_problem(
    random_problem_create: RandomProblemCreate,
    db: Annotated[Session, Depends(get_db)],
) -> RandomProblemResponse:
    logger.debug("Creating random problem: %s", random_problem_create)
    logger.info("Creating random problem for user_id: %s", random_problem_create.user_id)
    return create_random_problem_service(db, random_problem_create)


@router.patch(
    "/complete/{random_problem_id}",
    summary="ランダム問題を完了するAPIエンドポイント。",
    description="""
ユーザーがランダム問題を完了した際に呼び出されます。
ユーザーIDとランダム問題ID、ユーザーの位置情報、および画像URLを受け取り、問題のステータスを「completed」に更新します。
""",
)
async def complete_random_problem(
    random_problem_complete: RandomProblemComplete,
    random_problem_id: Annotated[
        int,
        Path(..., description="ID of the random problem to complete"),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> RandomProblemResponse:
    logger.debug("Completing random problem: %s", random_problem_complete)
    logger.info("Completing random problem with ID: %s", random_problem_id)
    return complete_problem_service(db, random_problem_id, random_problem_complete)


@router.patch(
    "/given-up/{random_problem_id}",
    summary="ランダム問題を諦めるAPIエンドポイント。",
    description="""
ユーザーがランダム問題を諦めた際に呼び出されます。
ユーザーIDとランダム問題IDを受け取り、問題のステータスを「given_up」に更新します。
""",
)
async def give_up_random_problem(
    random_problem_given_up: RandomProblemGivenUp,
    random_problem_id: Annotated[
        int,
        Path(..., description="ID of the random problem to give up"),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> RandomProblemResponse:
    logger.debug("Giving up random problem: %s", random_problem_given_up)
    logger.info("Giving up random problem with ID: %s", random_problem_id)
    return give_up_problem_service(db, random_problem_id, random_problem_given_up)
