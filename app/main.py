from datetime import timedelta

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from typing import Union
from pydantic import BaseModel
import boto3
import base64
import io
from app.auth import (
    authenticate_user,
    create_access_token,
    get_auth
)

from app.models import Login, Token, User, TokenData, Preferences, WeatherResponse
from app.fake_db import users_db, get_mongodb
from app.helpers import fetch_weather, set_user_preferences, get_user_preferences, set_user_profile_pic, get_user_profile_pic


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
async def get_preferences(_user: TokenData = Depends(get_auth), _db=Depends(get_mongodb)):
    return get_user_preferences(_db, _user.username)


@app.post("/users/me/preferences")
async def save_preferences(preferences: Preferences, _user: TokenData = Depends(get_auth),  _db=Depends(get_mongodb)):
    response_data = set_user_preferences(_db, _user.username, preferences.city)
    return JSONResponse(content=response_data)


@app.get("/users/me/profile_pic")
async def get_profile_pic(_user: TokenData = Depends(get_auth)):
    response_data = get_user_profile_pic(_user.username)
    return JSONResponse(content=response_data)


@app.post("/users/me/profile_pic")
async def save_profile_pic(picture: UploadFile = File(...), _user: TokenData = Depends(get_auth)):
    image_data = await picture.read()
    response_data = set_user_profile_pic(_user.username, image_data)
    return JSONResponse(content=response_data)


@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str, _user: TokenData = Depends(get_auth)):
    weather = fetch_weather(city)
    return WeatherResponse(city=city, weather=weather)
