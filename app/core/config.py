from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    app_title: str
    app_description: str
    database_url: str
    secret: str
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str| None = None
    authorization: str
    ertelecom_login: str
    bot_email: str
    bot_password: str
    bot_token: str
    api_url: str
    face_data: str
    
    class Config:
        env_file = '.env'
        

settings = Settings()
