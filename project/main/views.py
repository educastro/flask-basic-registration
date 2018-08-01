# project/main/views.py


#################
#### imports ####
#################

import datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import User
# from project.email import send_email
from project.token import generate_confirmation_token, confirm_token
from project import db, bcrypt
from project.email import send_email
from project.decorators import check_confirmed
from .forms import LoginForm, RegisterForm, ChangePasswordForm



################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
def home():
	return redirect(url_for('user.calculator'))