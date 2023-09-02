from typing import Optional, Dict
from contextlib import contextmanager

from pydantic import BaseModel
from pymongo import MongoClient

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


@contextmanager
def get_mongodb():
    try:
        with MongoClient() as client:
            db = client["preferences"]
            yield db
    except Exception as e:
        print(f'Error: {e}')
        raise
