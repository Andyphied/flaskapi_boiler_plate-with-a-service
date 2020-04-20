import datetime

from marshmallow import ValidationError
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
            email=data['email'],
            password=data['password'],
            registered_on=datetime.datetime.now()
        )
        save_changes(new_user)

    except Exception as e:
            raise InternalServerError

    else:
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201



def save_changes(data):
    db.session.add(data)
    db.session.commit()