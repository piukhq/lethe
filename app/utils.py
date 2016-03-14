from settings import BASE_URL
from urllib.parse import urljoin


def url_for(endpoint, *args):
    arg_string = '/'.join(args)
    return urljoin(BASE_URL, '{}/{}'.format(endpoint, arg_string))
