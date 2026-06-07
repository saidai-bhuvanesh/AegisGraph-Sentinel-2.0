import os
import datetime
from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: str  # subject / user identifier
    exp: int  # expiration timestamp (Unix epoch)
    iat: int  # issued at timestamp
    roles: list[str] = []  # optional role list
