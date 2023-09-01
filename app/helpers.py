import json

import requests
import boto3
from botocore.exceptions import ClientError

from fastapi import HTTPException

from app.config import config


def get_s3_client():
    return boto3.client('s3', region_name='us-east-1')


def get_user_preferences(username):
    s3 = get_s3_client()
    try:
        obj = s3.get_object(Bucket=config().user_preferences_bucket, Key=f'pref_{username}.json')
        body = obj['Body'].read().decode('utf-8')
        return json.loads(body)
    except s3.exceptions.NoSuchKey:
        return {}
    except ClientError as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=500, detail=str(e))


def set_user_preferences(username, city):
    s3 = get_s3_client()
    data = {"city": city}
    try:
        s3.put_object(Bucket=config().user_preferences_bucket, Key=f'pref_{username}.json', Body=json.dumps(data))
        return {"detail": "success"}
    except ClientError as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=500, detail=str(e))


def fetch_weather(city_name):
    url = f"http://wttr.in/{city_name}?format=%C+%t"
    response = requests.get(url)
    return response.text
