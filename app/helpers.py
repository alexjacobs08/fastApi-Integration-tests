import base64

import requests
import boto3

from fastapi import HTTPException

from app.config import config


def get_s3_client():
    return boto3.client('s3', region_name='us-east-1')


def get_user_preferences(_db, username: str) -> dict:
    try:
        with _db as db:
            collection = db.preferences
            result = collection.find_one({"username": username})
        if result:
            return {"city": result.get("city", "")}
        else:
            raise HTTPException(status_code=404, detail="Preferences not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def set_user_preferences(_db, username: str, city: str) -> dict:
    try:
        with _db as db:
            collection = db.preferences
            result = collection.update_one(
                {"username": username},
                {"$set": {"city": city}},
                upsert=True
            )
        if result.upserted_id or result.modified_count:
            return {"detail": "success"}
        else:
            raise HTTPException(status_code=500, detail="Database operation failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user_profile_pic(username: str) -> dict:
    s3 = get_s3_client()
    try:
        response = s3.get_object(Bucket=config().user_preferences_bucket, Key=f"profile_pics/{username}.png")
        image_data = response['Body'].read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return {"detail": "success", "image": base64_image}
    except s3.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail=str("No profile pic found"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def set_user_profile_pic(username: str, image_data: bytes) -> dict:
    s3 = get_s3_client()
    try:
        s3.put_object(Body=image_data, Bucket=config().user_preferences_bucket, Key=f"profile_pics/{username}.png")
        return {"detail": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_weather(city_name):
    url = f"http://wttr.in/{city_name}?format=%C+%t"
    response = requests.get(url)
    return response.text
