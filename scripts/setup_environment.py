from config.utils import get_env
import subprocess
import requests
import time
import os

BASE_URL = get_env("BASE_URL")
BINSHOPS_REPO = "https://github.com/binshops/prestashop-rest.git"
BINSHOPS_COMMIT = "c9007fbff64daed488a51267ff66fb9bf903c41f"
BINSHOPS_PATH = "binshopsrest"

SQL_DISABLE_ADMIN_SECURITY = """
UPDATE ps_configuration
SET value=0
WHERE name='PS_ADMIN_API_FORCE_DEBUG_SECURED'
"""


def ensure_environment() -> None:
    _ensure_playwright_browsers()
    _ensure_binshops_module()

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

def _ensure_playwright_browsers() -> None:
    print("Checking Playwright browsers...")

    result = subprocess.run(
        ["playwright", "install"],
        check=True,
    )

    if result.returncode != 0:
        raise RuntimeError("Failed to install Playwright browsers.")

    print("Playwright browsers are ready.")

def _ensure_binshops_module() -> None:
    if os.path.isdir(BINSHOPS_PATH):
        print("Binshops REST module already exists. Skipping clone...")
        return

    print("Cloning Binshops REST module...")
    subprocess.run(
        [
            "git",
            "clone",
            "--revision",
            BINSHOPS_COMMIT,
            BINSHOPS_REPO,
            BINSHOPS_PATH,
        ],
        check=True,
    )

    print("Binshops REST module cloned.")


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

        time.sleep(10)


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
