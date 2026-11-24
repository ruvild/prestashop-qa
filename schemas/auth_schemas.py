from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginUser(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    email: EmailStr
    firstname: str
    lastname: str
    id_default_group: int
    active: int | str
    is_guest: int | str
    logged: bool


class LoginSuccessData(BaseModel):
    status: Literal["success"]
    message: str
    customer_id: int
    session_data: int
    cart_count: int
    user: LoginUser


class LoginResponse(BaseModel):
    success: bool
    code: int
    psdata: LoginSuccessData | str | None = None
    message: str | None = None


class AccountInfoResponse(BaseModel):
    code: int
    success: bool
    psdata: LoginUser | None = None
    message: str | None = None


class LogoutResponse(BaseModel):
    code: int
    success: bool
    message: str


class AuthMethodResponse(BaseModel):
    success: bool
    code: int
    psdata: Any = None
    message: str
