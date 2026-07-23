import requests
from config.utils import url_joiner, get_env


class BaseClient:

    def __init__(self, auth_token: str) -> None:
        self.base_url = f"{get_env('BASE_URL')}/admin-api"
        self.session = requests.Session()
        self.auth_header = {"Authorization": f"Bearer {auth_token}"}

    def build_url(self, endpoint) -> str:
        return url_joiner(self.base_url, endpoint)
