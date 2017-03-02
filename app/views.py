import requests
from app.exceptions import HermesBadResponseError
from app.models import is_valid_token
from app.utils import url_for
from flask import Blueprint, render_template, request, flash
from werkzeug.utils import redirect
import settings

frontend = Blueprint('frontend', __name__)


@frontend.route('/password/account_updated')
def account_updated():
    return render_template('account_updated.html')


@frontend.route('/password/<link_token>', methods=['GET', 'POST'])
def new_password(link_token=None):
    if request.method == 'POST':
        password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_new_password')

        if password is None:
            flash('You must provide your new password.')
            return redirect(url_for('password', link_token))

        if confirm_password is None:
            flash('You must confirm your new password.')
            return redirect(url_for('password', link_token))

        if password != confirm_password:
            flash('The passwords you entered did not match. Please try again.')
            return redirect(url_for('password', link_token))

        reset_password_url = "{}/{}".format(settings.HERMES_URL, "/users/reset_password")
        response = requests.post(reset_password_url, data={'token': link_token, 'password': password})

        if response.status_code == 200:
            return redirect(url_for('password/account_updated'))
        elif response.status_code == 400:
            j = response.json()
            for element in j['password']:
                flash('This password is invalid. ' + element[26:])
            return redirect(url_for('password', link_token))
    else:
        try:
            if is_valid_token(link_token):
                return render_template('new_password.html')
            else:
                return render_template('link_expired.html')
        except HermesBadResponseError:
            flash('Sorry, something has gone wrong on our end. Give us some time to fix it, and try again later!')
            return render_template('error_page.html')
