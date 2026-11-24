import logging
import os
import subprocess
import time

import requests

from config.utils import get_env

logger = logging.getLogger(__name__)

BASE_URL = get_env("BASE_URL")
BINSHOPS_REPO = "https://github.com/binshops/prestashop-rest.git"
BINSHOPS_COMMIT = "eaeec19ca95f6b5d94c03cbf277133502b4248c3"
BINSHOPS_PATH = "binshopsrest"

SQL_DISABLE_ADMIN_SECURITY = """
UPDATE ps_configuration
SET value=0
WHERE name='PS_ADMIN_API_FORCE_DEBUG_SECURED'
"""


def ensure_environment() -> None:
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )

    _ensure_playwright_browsers()
    _ensure_binshops_module()

    if _is_environment_up():
        logger.info("Environment already running. Skipping container setup...")
        return

    logger.info("Starting Docker...")
    subprocess.run(
        ["docker", "compose", "up", "-d"],
        check=True,
    )

    _wait_until_ready()
    _disable_admin_security()


def _ensure_playwright_browsers() -> None:
    logger.info("Checking Playwright browsers...")

    subprocess.run(
        ["playwright", "install"],
        check=True,
    )

    logger.info("Playwright browsers are ready.")


def _ensure_binshops_module() -> None:
    if os.path.isdir(BINSHOPS_PATH):
        logger.info("Binshops REST module already exists. Skipping clone...")
        return

    logger.info("Cloning Binshops REST module...")
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

    logger.info("Binshops REST module cloned.")


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
                logger.info("PrestaShop is up and responding!")
                break
        except requests.RequestException:
            logger.info("Waiting for PrestaShop container initialization...")

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
            get_env("DB_USER"),
            f"-p{get_env('DB_ROOT_PASSWORD')}",
            get_env("DB_NAME"),
            "-e",
            SQL_DISABLE_ADMIN_SECURITY,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(result.stderr)

    logger.info("Admin API security check disabled.")
