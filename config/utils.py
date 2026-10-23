from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import re
from urllib.parse import urlparse
from typing import Any

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


def binshops_extractor(field: str, search_response: dict[str, Any]) -> list:
    return [product[field] for product in search_response["psdata"]["products"]]


def product_url_parser(url: str) -> dict:
    parsed_url = urlparse(url)

    product_match = re.search(
        r"/(?P<product_id>\d+)(?:-(?P<combination_id>\d+))?-[^/]+\.html$",
        parsed_url.path,
    )

    if not product_match:
        raise ValueError(f"Unexpected product URL format: {url}")

    attributes = {}
    if parsed_url.fragment:
        for attribute_id, group, value in re.findall(
            r"/(\d+)-([a-z]+)-([a-z]+)",
            parsed_url.fragment,
        ):
            attributes[group] = {
                "attribute_id": attribute_id,
                "value": value,
            }

    return {
        "product_id": int(product_match.group("product_id")),
        "combination_id": (
            int(product_match.group("combination_id"))
            if product_match.group("combination_id")
            else None
        ),
        "attributes": attributes,
    }
