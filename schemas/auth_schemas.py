from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str | None
    email: str | None
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username":"johndoe",
                "email":"john@gmail.com",
                "password":"johndoe",
                "is_staff":False,
                "is_active":True
            }
        }