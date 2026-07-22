import requests
import time
from config.utils import get_env
import os
import subprocess
from config.permissions import ALL_PERMISSIONS

SQL_DISABLE_ADMIN_SECURITY = """
UPDATE ps_configuration
SET value=0
WHERE name='PS_ADMIN_API_FORCE_DEBUG_SECURED'
"""


class EnvironmentProvisioner:

    def __init__(self):

        self.base_url = get_env("BASE_URL")
        self.admin_api_client_id = "presta-qa"

    def setup(self) -> str:
        self._start_environment()
        self._wait_until_ready()
        self._disable_admin_security()
        self._delete_api_client()
        secret = self._create_api_client()
        admin_api_token = self._generate_access_token(secret)
        return admin_api_token

    def teardown(self) -> None:
        self._delete_api_client()

    def _start_environment(self) -> None:
        subprocess.run(["docker", "compose", "up", "-d"], check=True)

    def _wait_until_ready(self) -> None:
        start = time.time()
        while True:
            try:
                requests.get(self.base_url, timeout=30)
                break
            except requests.RequestException:
                if time.time() - start > 300:
                    raise TimeoutError("PrestaShop failed to start.")
                time.sleep(2)

    def _disable_admin_security(self) -> None:
        result = subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "mysql",
                "mysql",
                "-u",
                f"{os.getenv('DB_USER')}",
                f"-p{os.getenv('DB_ROOT_PASSWORD')}",
                f"{os.getenv('DB_NAME')}",
                "-e",
                SQL_DISABLE_ADMIN_SECURITY,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)

        print("Admin API security check disabled.")

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
                print("API client doesn't exist. Continuing...")
                return
            raise Exception(result.stderr)

        print(f"Client {self.admin_api_client_id} deleted.")

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
                "--timeout=30000000",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        secret = result.stdout.strip()
        print(f"Client {self.admin_api_client_id} created.")
        return secret

    def _generate_access_token(self, secret: str) -> str:
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.admin_api_client_id,
            "client_secret": secret,
            "scope[]": ALL_PERMISSIONS,
        }
        res = requests.post(
            f"{self.base_url}/admin-api/access_token", data=payload, timeout=30
        )
        res.raise_for_status()
        access_token = res.json()["access_token"]
        print("Access token generated.")

        return access_token
