import datetime

from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError
from flask_jwt_extended import create_access_token
from service.blacklist_service import save_token
from database.models import User


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            authorized = user.check_password(data.get('password'))
            if not authorized:
                return UnauthorizedError

            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                                'status': 'success',
                                'message': 'Successfully logged in.',
                                'Authorization': auth_token.decode()
                }
                return response_object, 200
        
        except Exception as e:
            print(e)
            return InternalServerError


    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403