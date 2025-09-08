from pydantic import BaseModel, Field, EmailStr
from datetime import date
from backend.enums import FavoriteColor


class CreateUserProfile(BaseModel):
    uid: str = Field(max_length=128, min_length=1)
    display_name: str = Field(max_length=50, min_length=1)
    email: EmailStr
    birthday: date|None
    favorite_color: FavoriteColor|None


class UpdateUserProfile(BaseModel):
    display_name: str|None = Field(max_length=50, min_length=1)
    email: EmailStr|None
    birthday: date|None
    favorite_color: FavoriteColor|None


class ReadUserProfile(BaseModel):
    uid: str = Field(max_length=128, min_length=1)
    display_name: str = Field(max_length=50, min_length=1)
    email: EmailStr
    birthday: date|None
    favorite_color: FavoriteColor|None

    model_config = ConfigDict(from_attributes=True)


class PublicReadUserProfile(BaseModel):
    display_name: str = Field(max_length=50, min_length=1)
    email: EmailStr
    birthday: date|None
    favorite_color: FavoriteColor|None

    model_config = ConfigDict(from_attributes=True)