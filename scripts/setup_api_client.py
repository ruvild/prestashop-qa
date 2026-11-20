import logging
import subprocess

import requests

from config.permissions import ALL_PERMISSIONS
from config.utils import get_env, url_joiner

logger = logging.getLogger(__name__)


class ApiClientSetup:

    def __init__(self, worker_id: str = "master"):

        self.base_url = get_env("BASE_URL")
        self.admin_api_client_id = f"presta-qa-{worker_id}"

    def setup(self) -> str:

        self._delete_api_client()
        secret = self._create_api_client()
        admin_api_token = self._generate_access_token(secret)
        return admin_api_token

    def teardown(self) -> None:
        self._delete_api_client()

    def _delete_api_client(self) -> None:
        result = subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "--user",
                "www-data",
                "prestashop",
                "php",
                "bin/console",
                "prestashop:api-client",
                "delete",
                self.admin_api_client_id,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            if "not found" in result.stdout.lower():
                logger.info("API client doesn't exist. Continuing...")
                return
            raise Exception(result.stderr)

        logger.info("Client %s deleted.", self.admin_api_client_id)

    def _create_api_client(self) -> str:
        result = subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "--user",
                "www-data",
                "prestashop",
                "php",
                "bin/console",
                "prestashop:api-client",
                "create",
                self.admin_api_client_id,
                "--all-scopes",
                "--secret-only",
                "--timeout=3600",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        secret = result.stdout.strip()
        logger.info("Client %s created.", self.admin_api_client_id)
        return secret

    def _generate_access_token(self, secret: str) -> str:
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.admin_api_client_id,
            "client_secret": secret,
            "scope[]": ALL_PERMISSIONS,
        }
        res = requests.post(
            url_joiner(self.base_url, "admin-api/access_token"),
            data=payload,
            timeout=30,
        )
        res.raise_for_status()
        access_token = res.json()["access_token"]
        logger.info("Access token generated.")

        return access_token
