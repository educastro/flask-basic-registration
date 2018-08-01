from flask_wtf import Form
from wtforms import TextField, DecimalField, FloatField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import User


class LoginForm(Form):
    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    
    driverName = TextField(
        'driverName',
        validators=[DataRequired(), Length(min=3,max=50)]
    )

    carPrice = TextField(
        'carPrice',
        validators=[DataRequired()]
    )

    medianConsumption = TextField(
        'medianConsumption',
        validators=[DataRequired()]
    )

    medianDistance = TextField(
        'medianDistance',
        validators=[DataRequired()]
    )

    gasPrice = TextField(
        'gasPrice',
        validators=[DataRequired()]
    )

    taxesPrice = TextField(
        'taxesPrice',
        validators=[DataRequired()]
    )

    maintenancePrice = TextField(
        'maintenancePrice',
        validators=[DataRequired()]
    )

    securePrice = TextField(
        'securePrice',
        validators=[DataRequired()]
    )

    penaltiesPrice = TextField(
        'penaltiesPrice',
        validators=[DataRequired()]
    )

    parkingPrice = TextField(
        'parkingPrice',
        validators=[DataRequired()]
    )

    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])

    
    password = PasswordField(
        'password'
    )
    
    confirm = PasswordField(
        'Repeat password'
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            #self.email.errors.append("Email already registered")
            return True
        return True


class ChangePasswordForm(Form):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
)