import uuid
import datetime

from database.models import db, User
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError
""" 
    Handles All Of the User Related Services 

    save_new_user: Helps save the user data to the db

"""


def  save_new_user(data):
    
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return EmailAlreadyExistsError
    try:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.now()
        )
        save_changes(new_user)

    except Exception as e:
        print (e)
        raise InternalServerError

    else:
        return generate_token(new_user)


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401