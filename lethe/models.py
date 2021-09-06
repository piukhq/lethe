from typing import Optional, Tuple

import requests

from . import settings
from .exceptions import HermesBadResponseError


def is_valid_token(token: Optional[str]) -> bool:
    valid_token_url = "{}{}".format(settings.HERMES_URL, "/users/validate_reset_token")
    try:
        response = requests.post(valid_token_url, data={"token": token})
    except requests.exceptions.ConnectionError as e:
        raise HermesBadResponseError(f"Failed to connect to Hermes. Error: {e}")

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise HermesBadResponseError("Hermes returned error code {}".format(response.status_code))


def is_hermes_ready() -> Tuple[bool, str]:
    try:
        resp = requests.get(settings.HERMES_URL + "/healthz", timeout=2)
        if resp.status_code not in (200, 204, 404):
            return False, f"Hermes not available, status: {resp.status_code}"
    except Exception as err:
        return False, f"Hermes not available, error: {err}"

    return True, ""
