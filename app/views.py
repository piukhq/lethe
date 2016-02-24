from app.models import is_valid_token
from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/<link_token>')
def new_password(link_token=None):
    if is_valid_token(link_token):
        return render_template('new_password.html')
    else:
        return render_template('link_expired.html')
