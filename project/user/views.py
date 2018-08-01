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
            carPrice=form.carPrice.data.replace(",","."),
            medianConsumption=form.medianConsumption.data.replace(",","."),
            medianDistance=form.medianDistance.data.replace(",","."),
            gasPrice=form.gasPrice.data.replace(",","."),
            taxesPrice=form.taxesPrice.data.replace(",","."),
            maintenancePrice=form.maintenancePrice.data.replace(",","."),
            securePrice=form.securePrice.data.replace(",","."),
            penaltiesPrice=form.penaltiesPrice.data.replace(",","."),
            parkingPrice=form.parkingPrice.data.replace(",","."),
            email=form.email.data,
            password="test",
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

        car_annualDepreciation = round(((8 * float(user.carPrice))/100),2)
        car_annualSpendWithGasoline = round(((((float(user.medianDistance)/float(user.medianConsumption))*float(user.gasPrice))*30)*12),2)
        car_annualSpendWithParking = round((float(user.parkingPrice)*12),2)
        car_annualCost = round((car_annualSpendWithGasoline + car_annualSpendWithParking + float(user.penaltiesPrice) + float(user.maintenancePrice) + float(user.taxesPrice) + float(user.securePrice) + car_annualDepreciation),2)
        car_annualOpportunityCost = round(((float(user.carPrice) + car_annualCost) * (6.5/100)),2)
        car_annualSpendTotal = round((car_annualCost + car_annualOpportunityCost),2)

        uber_baseFare = 2.70
        uber_fixedCost = 1.00
        uber_costPerMinute = 0.18
        uber_costPerKM = 1.25
        uber_distancePerRun = round((float(user.medianDistance)/2),2)
        uber_timePerRun = round(((uber_distancePerRun * 60)/60),2)
        uber_dailyCost = round(((uber_baseFare + uber_fixedCost + (uber_costPerMinute * uber_timePerRun) + (uber_costPerKM * uber_distancePerRun))*2),2)
        uber_monthlyCost = round((uber_dailyCost * 30),2)
        uber_annualCost = round((uber_monthlyCost * 12),2) 
        uber_totalCost = round((uber_annualCost - car_annualOpportunityCost),2)

        taxi_baseFare = 0
        taxi_fixedCost = 5.24
        taxi_costPerMinute = 0.53
        taxi_costPerKM = 2.85
        taxi_distancePerRun = round((float(user.medianDistance)/2),2)
        taxi_timePerRun = round(((taxi_distancePerRun * 60)/60),2)
        taxi_dailyCost = round(((taxi_baseFare + taxi_fixedCost + (taxi_costPerMinute * taxi_timePerRun) + (taxi_costPerKM * taxi_distancePerRun))*2),2)
        taxi_monthlyCost = round((taxi_dailyCost * 30),2)
        taxi_annualCost = round((taxi_monthlyCost * 12),2) 
        taxi_totalCost = round((taxi_annualCost - car_annualOpportunityCost),2)

        taxi99_baseFare = 0
        taxi99_fixedCost = 2.38
        taxi99_costPerMinute = 0.19
        taxi99_costPerKM = 1.14
        taxi99_distancePerRun = round((float(user.medianDistance)/2),2)
        taxi99_timePerRun = round(((taxi99_distancePerRun * 60)/60),2)
        taxi99_dailyCost = round(((taxi99_baseFare + taxi99_fixedCost + (taxi99_costPerMinute * taxi99_timePerRun) + (taxi99_costPerKM * taxi99_distancePerRun))*2),2)
        taxi99_monthlyCost = round((taxi99_dailyCost * 30),2)
        taxi99_annualCost = round((taxi99_monthlyCost * 12),2) 
        taxi99_totalCost = round((taxi99_annualCost - car_annualOpportunityCost),2)

        html = render_template('user/debug.html', driverName = user.driverName, carPrice = user.carPrice, medianConsumption = user.medianConsumption, medianDistance = user.medianDistance, gasPrice = user.gasPrice, taxesPrice = user.taxesPrice, maintenancePrice = user.maintenancePrice, securePrice = user.securePrice, penaltiesPrice = user.penaltiesPrice, parkingPrice = user.parkingPrice, email = user.email, car_annualDepreciation = car_annualDepreciation, car_annualSpendWithGasoline = car_annualSpendWithGasoline, car_annualSpendWithParking = car_annualSpendWithParking, car_annualCost = car_annualCost, car_annualOpportunityCost = car_annualOpportunityCost, car_annualSpendTotal = car_annualSpendTotal, uber_baseFare = uber_baseFare, uber_fixedCost = uber_fixedCost, uber_costPerMinute = uber_costPerMinute, uber_costPerKM = uber_costPerKM, uber_distancePerRun = uber_distancePerRun, uber_timePerRun = uber_timePerRun, uber_dailyCost = uber_dailyCost, uber_monthlyCost = uber_monthlyCost, uber_annualCost = uber_annualCost, uber_totalCost = uber_totalCost, taxi_baseFare = taxi_baseFare, taxi_fixedCost = taxi_fixedCost, taxi_costPerMinute = taxi_costPerMinute, taxi_costPerKM = taxi_costPerKM, taxi_distancePerRun = taxi_distancePerRun, taxi_timePerRun = taxi_timePerRun, taxi_dailyCost = taxi_dailyCost, taxi_monthlyCost = taxi_monthlyCost, taxi_annualCost = taxi_annualCost, taxi_totalCost = taxi_totalCost, taxi99_baseFare = taxi99_baseFare, taxi99_fixedCost = taxi99_fixedCost, taxi99_costPerMinute = taxi99_costPerMinute, taxi99_costPerKM = taxi99_costPerKM, taxi99_distancePerRun = taxi99_distancePerRun, taxi99_timePerRun = taxi99_timePerRun, taxi99_dailyCost = taxi99_dailyCost, taxi99_monthlyCost = taxi99_monthlyCost, taxi99_annualCost = taxi99_annualCost, taxi99_totalCost = taxi99_totalCost)
        #html = render_template('user/activate.html', personName=user.driverName, annualSpendWithTheCar=annualSpendWithTheCar, annualSpendWithUber=annualSpendWithUber)
        subject = "Resultado: E ai, o que vale mais a pena? Carro ou Uber?"


        #token = generate_confirmation_token(user.email)
        #confirm_url = url_for('user.confirm_email', token=token, _external=True)
        #html = render_template('user/activate.html', confirm_url=confirm_url)
        #subject = "Please confirm your email"
        send_email(user.email, subject,html)

        #login_user(user)
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