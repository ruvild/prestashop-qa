from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import re

load_dotenv()


def get_env(variable_name: str) -> str:
    value = os.getenv(variable_name)
    if not value:
        raise RuntimeError(f"Environment variable '{variable_name}' is not set.")
    return value


def url_joiner(base_url: str, endpoint: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", endpoint.lstrip("/"))


def extract_product_ids(id_list: list) -> list:
    return [int(re.sub(r"\D", "", product_id)) for product_id in id_list]
