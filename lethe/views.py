from typing import Optional, Tuple, Union

import requests

from flask import Blueprint, flash, jsonify, render_template, request
from werkzeug.utils import redirect
from werkzeug.wrappers import Response as WerkResponse

from . import settings
from .exceptions import HermesBadResponseError
from .models import is_hermes_ready, is_valid_token
from .prometheus import handle_metrics, request_counter

internal = Blueprint("internal", __name__)
frontend = Blueprint("frontend", __name__, url_prefix="/password")

internal.add_url_rule("/metrics", "metrics", view_func=handle_metrics)

Response = Union[str, Tuple[str, int], WerkResponse]


@internal.route("/healthz")
def healthz() -> Response:
    return "", 204


@internal.route("/livez")
def livez() -> Response:
    return "", 204


@internal.route("/readyz")
def readyz() -> Response:
    # Check if hermes is up as its a direct dependency
    ok, output = is_hermes_ready()
    if not ok:
        output = jsonify({"error": output})  # type: ignore

    return output, 204 if ok else 500


@frontend.route("/account_updated")
def account_updated() -> Response:
    return render_template("account_updated.html")


def url(endpoint: str) -> str:
    url_prefix = frontend.url_prefix.lstrip("/")  # type: ignore
    return "{}/{}/{}".format(settings.EXTERNAL_SERVER_NAME, url_prefix, endpoint.lstrip("/"))


@frontend.route("/<link_token>", methods=["GET", "POST"])
def new_password(link_token: Optional[str] = None) -> Response:
    if request.method == "POST" and link_token:
        password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_new_password")

        if password is None:
            flash("You must provide your new password.")
            return redirect(url(link_token))

        if confirm_password is None:
            flash("You must confirm your new password.")
            return redirect(url(link_token))

        if password != confirm_password:
            flash("The passwords you entered did not match. Please try again.")
            return redirect(url(link_token))

        reset_password_url = "{}{}".format(settings.HERMES_URL, "/users/reset_password")
        response = requests.post(reset_password_url, data={"token": link_token, "password": password})

        if response.status_code == 200:
            request_counter.labels(template="account_updated").inc()
            return redirect(url("account_updated"))
        elif response.status_code == 400:
            err = "Password should be 8 or more characters, with at least 1 uppercase, 1 lowercase and a number"
            flash(err)
            return redirect(url(link_token))
        else:
            request_counter.labels(template="link_expired").inc()
            return render_template("link_expired.html")
    else:
        try:
            if is_valid_token(link_token):
                request_counter.labels(template="new_password").inc()
                return render_template("new_password.html")
            else:
                request_counter.labels(template="link_expired").inc()
                return render_template("link_expired.html")
        except HermesBadResponseError:
            flash("Sorry, something has gone wrong on our end. Give us some time to fix it, and try again later!")
            request_counter.labels(template="error_page").inc()
            return render_template("error_page.html")
