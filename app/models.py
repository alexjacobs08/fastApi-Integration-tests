from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    jwt: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class Preferences(BaseModel):
    city: str


class WeatherResponse(BaseModel):
    city: str
    weather: str
