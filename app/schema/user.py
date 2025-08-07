from pydantic import BaseModel


# 将来的にemailなどのフィールドを追加する可能性がありますが、
# 現時点では空のベースクラスを使用しています。
class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
