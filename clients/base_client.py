import requests
from config.utils import url_joiner, get_env


class BaseClient:

    def __init__(self) -> None:
        self.base_url = f"{get_env('BASE_URL')}/admin-api"
        self.session = requests.Session()
        self.auth_header = {"Authorization": f"Bearer {get_env("AUTH_KEY")}"}

    def build_url(self, endpoint) -> str:
        return url_joiner(self.base_url, endpoint)
