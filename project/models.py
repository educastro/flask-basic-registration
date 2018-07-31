# project/models.py


import datetime

from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    driverName = db.Column(db.String, nullable=False)
    carPrice = db.Column(db.Float, nullable=False)
    medianConsumption = db.Column(db.Float, nullable=False)
    medianDistance = db.Column(db.Float, nullable=False)
    gasPrice = db.Column(db.Float, nullable=False)
    taxesPrice = db.Column(db.Float, nullable=True)
    maintenancePrice = db.Column(db.Float, nullable=True)
    securePrice = db.Column(db.Float, nullable=True)
    penaltiesPrice = db.Column(db.Float, nullable=True)
    parkingPrice = db.Column(db.Float, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, driverName, carPrice, medianConsumption, medianDistance, gasPrice, taxesPrice, maintenancePrice, securePrice, penaltiesPrice, parkingPrice, email, password, confirmed, paid=False, admin=False, confirmed_on=None):
        self.driverName = driverName
        self.carPrice = carPrice
        self.medianConsumption = medianConsumption   
        self.medianDistance = medianDistance
        self.gasPrice = gasPrice
        self.taxesPrice = taxesPrice
        self.maintenancePrice = maintenancePrice
        self.securePrice = securePrice
        self.penaltiesPrice = penaltiesPrice
        self.parkingPrice = parkingPrice
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)
