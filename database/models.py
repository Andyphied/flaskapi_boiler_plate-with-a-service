import datetime

from sqlalchemy.ext.hybrid import  hybrid_property
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from app.config import key


flask_bcrypt = Bcrypt()
ma = Marshmallow()
db = SQLAlchemy()

"""
The following codes describe the Table as it is in the Database and its Schema.
There are a total of two tables in our Database: 
    - The Car Service Table
    - The User Table
    - Black List Token Table

"""


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


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
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    _password_hash = db.Column('password', db.String(100))
    
    """
    password: ensures password attribute is read only
    hash_password: coverts password to hashs
    check_password: confirms if password matches user password in the database

    """

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext):
        self._password_hash = flask_bcrypt.generate_password_hash(plaintext).decode('utf8')


    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self._password_hash, password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'                                                                        

    

    def __repr__(self):
        return "<User '{}'>".format(self.username)



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
    public_id = ma.auto_field
    username = ma.auto_field
    password = ma.auto_field