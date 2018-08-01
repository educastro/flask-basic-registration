# project/user/views.py


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

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            driverName=form.driverName.data,
            carPrice=form.carPrice.data,
            medianConsumption=form.medianConsumption.data,
            medianDistance=form.medianDistance.data,
            gasPrice=form.gasPrice.data,
            taxesPrice=form.taxesPrice.data,
            maintenancePrice=form.maintenancePrice.data,
            securePrice=form.securePrice.data,
            penaltiesPrice=form.penaltiesPrice.data,
            parkingPrice=form.parkingPrice.data,
            email=form.email.data,
            password="test",
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()


        annualSpendWithTheCar = user.medianConsumption
        annualSpendWithUber = user.gasPrice

        html = render_template('user/activate.html', personName=user.driverName, annualSpendWithTheCar=annualSpendWithTheCar, annualSpendWithUber=annualSpendWithUber)
        subject = "Resultado: E ai, o que vale mais a pena? Carro ou Uber?"


        #token = generate_confirmation_token(user.email)
        #confirm_url = url_for('user.confirm_email', token=token, _external=True)
        #html = render_template('user/activate.html', confirm_url=confirm_url)
        #subject = "Please confirm your email"
        send_email(user.email, subject,html)

        login_user(user)
        flash('A confirmation email has been sent via email', 'success')

        return redirect(url_for('user.calculator'))

    return render_template('user/calculator.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)

@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():  
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account', 'success')
    return render_template('user/unconfirmed.html')

@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'sucess')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))