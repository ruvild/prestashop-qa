from typing import Any
from requests import Response
from clients.binshops.base_client import BaseClient
from schemas.auth_schemas import (
    AccountInfoResponse,
    AuthMethodResponse,
    LoginResponse,
    LogoutResponse,
)


class AuthClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "login"

    def login(
        self,
        email: str | None = None,
        password: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> LoginResponse:
        if payload is None:
            payload = {}
            if email is not None:
                payload["email"] = email
            if password is not None:
                payload["password"] = password

        url = self.build_url(self.endpoint)
        res = self.session.post(url, json=payload)
        res.raise_for_status()
        return LoginResponse.model_validate(res.json())

    def send_unsupported_method(self, method: str = "GET") -> AuthMethodResponse:
        url = self.build_url(self.endpoint)
        res: Response = self.session.request(method, url)
        res.raise_for_status()
        return AuthMethodResponse.model_validate(res.json())

    def get_account_info(self) -> AccountInfoResponse:
        url = self.build_url("accountInfo")
        res = self.session.get(url)
        res.raise_for_status()
        return AccountInfoResponse.model_validate(res.json())

    def logout(self) -> LogoutResponse:
        url = self.build_url("logout")
        res = self.session.get(url)
        res.raise_for_status()
        return LogoutResponse.model_validate(res.json())
