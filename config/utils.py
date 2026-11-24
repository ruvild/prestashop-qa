import os
import re
import subprocess
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

from dotenv import load_dotenv

from schemas.product_schemas import BinshopsProductListResponse

load_dotenv()


def get_env(variable_name: str) -> str:
    value = os.getenv(variable_name)
    if not value:
        raise RuntimeError(f"Environment variable '{variable_name}' is not set.")
    return value


def url_joiner(base_url: str, endpoint: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", endpoint.lstrip("/"))


def extract_product_ids(id_list: list[str | None]) -> list[int]:
    return [
        int(re.sub(r"\D", "", product_id))
        for product_id in id_list
        if product_id is not None
    ]


def binshops_product_extractor(
    field: str, search_response: BinshopsProductListResponse
) -> list[Any]:
    assert search_response.psdata is not None, "Missing psdata in search response"
    return [getattr(product, field) for product in search_response.psdata.products]


def product_url_parser(url: str) -> dict[str, Any]:
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


def get_order_id_from_url(url: str) -> int:
    query_params = parse_qs(urlparse(url).query)
    return int(query_params["id_order"][0])


def stock_changer(product_id: int, stock_quantity: int) -> None:
    # PrestaShop's Admin API does not expose a product stock update endpoint,
    # so stock quantities are adjusted directly in MySQL for test setup.
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "mysql",
            "mysql",
            "-u",
            get_env("DB_USER"),
            f"-p{get_env('DB_ROOT_PASSWORD')}",
            get_env("DB_NAME"),
            "-e",
            f"""
            UPDATE ps_stock_available
            SET quantity = {stock_quantity}
            WHERE id_product = {product_id}
            """,
        ],
        check=True,
    )
