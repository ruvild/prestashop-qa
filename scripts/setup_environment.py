from config.utils import get_env
import subprocess
import requests
import time
import os

BASE_URL = get_env("BASE_URL")

SQL_DISABLE_ADMIN_SECURITY = """
UPDATE ps_configuration
SET value=0
WHERE name='PS_ADMIN_API_FORCE_DEBUG_SECURED'
"""


def ensure_environment():
    if _is_environment_up():
        print("Environment already running. Skipping container setup...")
        return
    print("Starting Docker...")
    subprocess.run(
        ["docker", "compose", "up", "-d"],
        check=True,
    )

    _wait_until_ready()
    _disable_admin_security()


def _is_environment_up() -> bool:
    try:
        res = requests.get(BASE_URL, timeout=10)
        return res.status_code == 200
    except requests.RequestException:
        return False


def _wait_until_ready() -> None:
    start = time.time()
    while True:
        try:
            res = requests.get(BASE_URL, timeout=5)
            if res.ok:
                print("\nPrestaShop is up and responding!")
                break
        except requests.RequestException:
            print("Waiting for PrestaShop container initialization...")

        if time.time() - start > 300:
            raise TimeoutError("PrestaShop failed to start within 5 minutes.")

        time.sleep(5)


def _disable_admin_security() -> None:
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
