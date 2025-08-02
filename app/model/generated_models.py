import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Double,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (PrimaryKeyConstraint("user_id", name="users_pkey"),)

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    random_problems: Mapped[list["RandomProblems"]] = relationship(
        "RandomProblems",
        back_populates="user",
    )


class RandomProblems(Base):
    __tablename__ = "random_problems"
    __table_args__ = (
        CheckConstraint(
            """status::text = ANY (ARRAY['pending'::character varying,
            'completed'::character varying, 'given_up'::character varying]::text[])""",
            name="random_problems_status_check",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            ondelete="CASCADE",
            name="random_problems_user_id_fkey",
        ),
        PrimaryKeyConstraint("random_problem_id", name="random_problems_pkey"),
    )

    random_problem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[float] = mapped_column(Double(53))
    longitude: Mapped[float] = mapped_column(Double(53))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    status: Mapped[str] = mapped_column(String(50))
    ended_at: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    image_url: Mapped[str | None] = mapped_column(String(255))

    user: Mapped["Users"] = relationship("Users", back_populates="random_problems")
