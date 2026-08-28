import requests
from config.utils import url_joiner, get_env


class BinshopsBaseClient:
    def __init__(self):
        self.base_url = f"{get_env('BASE_URL')}/rest"
        self.session = requests.Session()

    def build_url(self, endpoint: str) -> str:
        return url_joiner(self.base_url, endpoint)
