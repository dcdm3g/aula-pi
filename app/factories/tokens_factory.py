from typing import TypedDict
from enum import Enum
import jwt
import os

class Role(Enum):
  user = "user"
  admin = "admin"

class TokensFactoryRequest(TypedDict):
  id: str
  email: str
  role: Role

class TokensFactoryResponse(TypedDict):
  access_token: str
  refresh_token: str

def tokens_factory(data: TokensFactoryRequest) -> TokensFactoryResponse:
  return {
    "access_token": jwt.encode({ 
      "sub": data.get('id'),
      "email": data.get('email'),
      "role": data.get('role'),
    }, os.environ.get('JWT_SECRET')),
    "refresh_token": jwt.encode({
      "sub": data.get('id'),
    }, os.environ.get('JWT_SECRET')),
  }