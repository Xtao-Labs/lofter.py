import asyncio
import os
import warnings
from pathlib import Path
from typing import Optional

import pytest
from dotenv import load_dotenv

env_path = Path(".env")
if env_path.exists():
    load_dotenv()


@pytest.fixture(scope="session")
def event_loop():  # skipcq: PY-D0003
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        loop = asyncio.get_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def login_auth_key() -> Optional[str]:  # skipcq: PY-D0003
    _login_auth_key = os.environ.get("LOGIN_AUTH_KEY")
    if not _login_auth_key:
        warnings.warn(UserWarning("No login auth key set"), stacklevel=2)
        return None
    return _login_auth_key
