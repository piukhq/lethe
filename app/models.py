import requests
import settings
from app.exceptions import HermesBadResponseError


def is_valid_token(token):
    valid_token_url = '{}{}'.format(settings.HERMES_URL, '/users/validate_reset_token')
    try:
        response = requests.post(valid_token_url, data={'token': token})
    except requests.exceptions.ConnectionError as e:
        raise HermesBadResponseError(f"Failed to connect to Hermes. Error: {e}")
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise HermesBadResponseError('Hermes returned error code {}'.format(response.status_code))
