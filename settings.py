from environment import env_var, read_env
import os


read_env()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = env_var('LETHE_DEBUG', False)

DEV_PORT = env_var('DEV_PORT', 5000)
DEV_HOST = env_var('DEV_HOST', '127.0.0.1')

BASE_URL = env_var('LETHE_URL', 'http://{}:{}'.format(DEV_HOST, DEV_PORT))
HERMES_URL = env_var('HERMES_URL', 'http://dev.hermes.loyaltyangels.local')

# this will be prefixed onto any redirects sent to the user.
# if set, it must include the http scheme (probably http:// or https://), and it must not end in a forward slash.
# example: https://api.chingrewards.com
EXTERNAL_SERVER_NAME = env_var('EXTERNAL_SERVER_NAME', '')

STATIC_URL = env_var('LETHE_STATIC_URL', '/static/')

SECRET_KEY = '\xb9\xd1\xc13\xf3\x04\xdf\x89\xbd\xca\x8e\x16\xda\xcaj\x04\x88\xd1\x13;\xcc\xb8\x927'
