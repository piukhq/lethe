import requests
from app.models import is_valid_token
from flask import Blueprint, render_template, request, flash, url_for
from werkzeug.utils import redirect
import settings

frontend = Blueprint('frontend', __name__)


@frontend.route('/account_updated')
def account_updated():
    return render_template('account_updated.html')


@frontend.route('/')
@frontend.route('/<link_token>', methods=['GET', 'POST'])
def new_password(link_token=None):
    if request.method == 'POST':
        password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_new_password')

        if password is None:
            flash('You must provide your new password.')
            return redirect(url_for('frontend.new_password', link_token=link_token))

        if confirm_password is None:
            flash('You must confirm your new password.')
            return redirect(url_for('frontend.new_password', link_token=link_token))

        if password != confirm_password:
            flash('The passwords you entered did not match. Please try again.')
            return redirect(url_for('frontend.new_password', link_token=link_token))

        reset_password_url = "{}/{}".format(settings.HERMES_URL, "/users/reset_password")
        requests.post(reset_password_url, data={'token': link_token})

        return redirect(url_for('frontend.account_updated'))
    else:
        if is_valid_token(link_token):
            return render_template('new_password.html')
        else:
            return render_template('link_expired.html')
