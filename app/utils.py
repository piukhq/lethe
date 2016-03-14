from settings import BASE_URL
from urllib.parse import urljoin


def url_for(endpoint, *args):
    if args is None:
        return urljoin(BASE_URL, endpoint)
    else:
        arg_string = '/'.join(args)
        return urljoin(BASE_URL, '{}/{}'.format(endpoint, arg_string))
