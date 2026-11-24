import requests

from config.utils import get_env, url_joiner


class BaseClient:
    DEFAULT_TIMEOUT = 30

    def __init__(
        self, create_session: bool = True, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        self.base_url = url_joiner(get_env("BASE_URL"), "rest")
        self.timeout = timeout
        if create_session:
            self.session = requests.Session()

    def build_url(self, endpoint: str) -> str:
        return url_joiner(self.base_url, endpoint)
