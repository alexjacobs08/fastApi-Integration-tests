from datetime import timedelta

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends


from app.auth import (
    authenticate_user,
    create_access_token,
    get_auth
)

from app.models import Login, Token, User, TokenData, Preferences, WeatherResponse
from app.fake_db import users_db
from app.helpers import fetch_weather, set_user_preferences, get_user_preferences


app = FastAPI()


@app.post("/login", response_model=Token)
async def login(_login: Login):
    user = authenticate_user(users_db, _login.username, _login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"jwt": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(_user: TokenData = Depends(get_auth)):
    user = users_db.get(_user.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/me/preferences", response_model=Preferences)
async def get_preferences(_user: TokenData = Depends(get_auth)):
    return get_user_preferences(_user.username)


@app.post("/users/me/preferences")
async def save_preferences(preferences: Preferences, _user: TokenData = Depends(get_auth)):
    response_data = set_user_preferences(_user.username, preferences.city)
    return JSONResponse(content=response_data)


@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str, _user: TokenData = Depends(get_auth)):
    weather = fetch_weather(city)
    return WeatherResponse(city=city, weather=weather)
