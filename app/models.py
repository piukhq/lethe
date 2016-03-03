import requests
import settings


def is_valid_token(token):
    valid_token_url = "{}/{}".format(settings.HERMES_URL, "/users/validate_reset_token")
    response = requests.post(valid_token_url, data={'token': token})
    if response.status_code == 200:
        return True
    else:
        return False
