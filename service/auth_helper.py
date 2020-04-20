import datetime

from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError
from flask_jwt_extended import create_access_token

from database.models import User


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            authorized = user.check_password(data.get('password'))
            if not authorized:
                return UnauthorizedError

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            response_object = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'Authorization': access_token
            }
            return response_object, 200
        
        except Exception as e:
            print(e)
            return InternalServerError