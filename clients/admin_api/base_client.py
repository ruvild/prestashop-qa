import requests

from config.utils import get_env, url_joiner


class BaseClient:
    DEFAULT_TIMEOUT = 30

    def __init__(self, auth_token: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.base_url = url_joiner(get_env("BASE_URL"), "admin-api")
        self.session = requests.Session()
        self.auth_header = {"Authorization": f"Bearer {auth_token}"}
        self.timeout = timeout

    def build_url(self, endpoint: str) -> str:
        return url_joiner(self.base_url, endpoint)
