import datetime
import hashlib
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

from schemas.user_schema import User
from settings import settings


class WrongPassword(Exception):
    detail = 'Неверный пароль'


class NotValidToken(Exception):
    detail = 'Передан невалидный токен'


class ExpiredToken(Exception):
    detail = 'Срок действия токена закончился'


class AuthService:
    SALT = settings.SALT_FOR_PASSWORD

    def __init__(self, time_now=None):
        self.jwt_secret: str = settings.JWT_SECRET_KEY
        self.jwt_refresh_secret: str = settings.JWT_REFRESH_SECRET_KEY
        self.algorithm: str = settings.ALGORITHM
        self.access_token_expire: str = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire: str = settings.REFRESH_TOKEN_EXPIRE_MINUTES
        self.time_now = time_now or datetime.datetime.utcnow()

    @classmethod
    def hash_password(cls, password: str):
        res = hashlib.md5((password + cls.SALT).encode())
        return res.hexdigest()

    @staticmethod
    def verify_password(password: str, db_password: str) -> bool:
        if password == db_password:
            return True
        raise WrongPassword

    def validate_token(self, token: str, is_refresh: bool = False) -> User:
        secret = self.jwt_secret
        if is_refresh:
            secret = self.jwt_refresh_secret
        print(secret, token)
        try:
            payload = jwt.decode(token, secret, self.algorithm)
        except ExpiredSignatureError:
            raise ExpiredToken
        except JWTError:
            raise NotValidToken

        return User(**payload['user'])

    def build_payload(self, user: User, expire_token) -> dict:
        payload = {
            'iat': self.time_now,
            'exp': self.time_now + datetime.timedelta(minutes=expire_token),
            'sub': str(user.id),
            'user': {
                'id': str(user.id),
                'email': user.email
            },
            'typ': 'Bearer'
        }
        return payload

    def _create_access_token(self, user: User):
        payload = self.build_payload(user, self.access_token_expire)
        return jwt.encode(payload, self.jwt_secret, self.algorithm)

    def _create_refresh_token(self, user: User):
        payload = self.build_payload(user, self.refresh_token_expire)
        return jwt.encode(payload, self.jwt_refresh_secret, self.algorithm)

    def create_jwt_tokens(self, user: User):
        return {
            'access_token': self._create_access_token(user),
            'refresh_token': self._create_refresh_token(user)
        }
