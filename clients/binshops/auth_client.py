from typing import Any

from playwright.sync_api import APIRequestContext
from requests import Response

from clients.binshops.base_client import BaseClient
from schemas.auth_schemas import (
    AccountInfoResponse,
    AuthMethodResponse,
    LoginResponse,
    LogoutResponse,
)


class AuthClient(BaseClient):
    def __init__(
        self,
        request_context: APIRequestContext | None = None,
        timeout: int = BaseClient.DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(create_session=request_context is None, timeout=timeout)
        self.endpoint = "login"
        self.request = request_context

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
        if self.request is not None:
            res = self.request.post(url, data=payload, timeout=self.timeout * 1000)
            assert res.ok, f"Login failed: {res.status} {res.text()}"
            return LoginResponse.model_validate(res.json())

        res = self.session.post(url, json=payload, timeout=self.timeout)
        res.raise_for_status()
        return LoginResponse.model_validate(res.json())

    def send_unsupported_method(self, method: str = "GET") -> AuthMethodResponse:
        url = self.build_url(self.endpoint)
        res: Response = self.session.request(method, url, timeout=self.timeout)
        res.raise_for_status()
        return AuthMethodResponse.model_validate(res.json())

    def get_account_info(self) -> AccountInfoResponse:
        url = self.build_url("accountInfo")
        if self.request is not None:
            res = self.request.get(url, timeout=self.timeout * 1000)
            assert res.ok, f"Failed to fetch account info: {res.status} {res.text()}"
            return AccountInfoResponse.model_validate(res.json())

        res = self.session.get(url, timeout=self.timeout)
        res.raise_for_status()
        return AccountInfoResponse.model_validate(res.json())

    def logout(self) -> LogoutResponse:
        url = self.build_url("logout")
        res = self.session.get(url, timeout=self.timeout)
        res.raise_for_status()
        return LogoutResponse.model_validate(res.json())
