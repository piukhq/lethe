#!/usr/bin/env python
import os

import settings

from flask_script import Manager, Server, Shell

from lethe import app

app.config.SWAGGER_UI_DOC_EXPANSION = "list"
manager = Manager(app)

# access python shell with context
manager.add_command("shell", Shell(make_context=lambda: {"app": app}), use_ipython=True)

# run the app
manager.add_command("runserver", Server(port=settings.DEV_PORT, host=settings.DEV_HOST, threaded=True))

HERE = os.path.abspath(os.path.dirname(__file__))
UNIT_TEST_PATH = os.path.join(HERE, "tests")

if __name__ == "__main__":
    manager.run()
