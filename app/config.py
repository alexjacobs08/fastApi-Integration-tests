from pydantic import BaseModel


class AppConfig(BaseModel):
    user_preferences_bucket: str = 'fastAPI-example-app-user-preferences-store'


def config():
    return AppConfig()
