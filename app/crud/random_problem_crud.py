from app.crud.base import BaseCRUD
from app.model.generated_models import RandomProblems
from app.schema.random_problem import (
    RandomProblemComplete,
    RandomProblemForDB,
)


class RandomProblemCRUD(BaseCRUD):
    def create(self, data: RandomProblemForDB) -> RandomProblems:
        """Create a new random problem in the database."""
        db_problem = RandomProblems(**data.model_dump())
        self.db.add(db_problem)
        self.db.commit()
        self.db.refresh(db_problem)
        return db_problem

    def read(self, record_id: int) -> RandomProblems | None:
        """Read a record by its ID."""
        return (
            self.db.query(RandomProblems)
            .filter(RandomProblems.random_problem_id == record_id)
            .first()
        )

    def read_by_user_id(self, user_id: int) -> list[RandomProblems]:
        """Read random problems by user_id."""
        return self.db.query(RandomProblems).filter(RandomProblems.user_id == user_id).all()

    def update(self, problem_id: int, data: RandomProblemComplete) -> RandomProblems | None:
        """Update a random problem."""
        problem = (
            self.db.query(RandomProblems)
            .filter(RandomProblems.random_problem_id == problem_id)
            .first()
        )
        if problem:
            for key, value in data.model_dump().items():
                setattr(problem, key, value)
            self.db.commit()
            self.db.refresh(problem)
        return problem
