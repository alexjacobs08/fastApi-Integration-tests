from typing import Optional, Dict

from pydantic import BaseModel

from app.auth import get_password_hash


class UserInDB(BaseModel):
    username: str
    email: Optional[str] = None
    hashed_password: str


users_db: Dict[str, UserInDB] = {
    "alexjacobs": UserInDB(
        username="alexjacobs",
        email="alex@example.com",
        hashed_password=get_password_hash("secret"),
    )
}
