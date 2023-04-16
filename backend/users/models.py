from typing import Optional

from tortoise import fields
from tortoise.exceptions import DoesNotExist
from app.core.models import BaseDBModel
from typing import Tuple

from passlib import pwd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseDBModel):

    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'users'

    class PydanticMeta:
        computed = ["full_name"]
    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.username

    def set_password(self, raw_password: str):
        self.password_hash = pwd_context.hash(raw_password)
        self.save()

    def check_password(self, raw_password: str):
        return pwd_context.hash(raw_password) == self.password_hash

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        try:
            return cls.get(email=email)
        except DoesNotExist:
            return None

    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        try:
            return cls.get(username=username)
        except DoesNotExist:
            return None
