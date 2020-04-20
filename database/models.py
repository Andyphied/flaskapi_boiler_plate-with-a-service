from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()
ma = Marshmallow()
db = SQLAlchemy()

class CarServiceDataModel(db.Model):
    __tablename__ = "car_service_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_model = db.Column(db.String(255), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, unique=True)

class User(db.Model):
    __tablename__ = "user"
    
    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    password_hash = db.Column(db.String(100))

    @property
    def password(self, password):
        raise AttributeError('password: write-only field')

    @password.setter
    def hash_password(self):
        self.password = flask_bcrypt.generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)


class CarServiceDataSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CarServiceDataModel
    
    car_model = ma.auto_field
    date = ma.auto_field

class  UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field
    email = ma.auto_field
    registered_on = ma.auto_field
    password = ma.auto_field

