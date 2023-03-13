from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import ValidationError

import kori.app.services.user as user_service
from kori.app.core.config import Settings
from kori.app.core.exceptions import AuthException
from kori.app.schemas.user import TokenData, UserSchema

config = Settings()


def create_access_token(user: UserSchema, expiry_duration: timedelta | None = None) -> str:
    if expiry_duration:
        expiry = datetime.utcnow() + expiry_duration
    else:
        expiry = datetime.utcnow() + timedelta(minutes=int(config.access_token_expire_minutes))
    token_data = TokenData(user_id=str(user.id), org_id=str(user.org_id), exp=int(expiry.timestamp()))
    encoded_jwt = jwt.encode(token_data.dict(), config.secret_key, algorithm=config.algorithm)
    return encoded_jwt


def verify_access_token(access_token: str) -> UserSchema:
    try:
        payload = jwt.decode(access_token, config.secret_key, algorithms=[config.algorithm])
        token_data = TokenData.parse_obj(payload)
    except (JWTError, ValidationError):
        raise AuthException(message="Invalid token detected")
    user = user_service.get_user_by_id(UUID(token_data.user_id))
    if user is None or user.org_id != UUID(token_data.org_id):
        raise AuthException(message="Invalid token detected")
    return user


def verify_access(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserSchema:
    access_token = credentials.credentials
    return verify_access_token(access_token)
