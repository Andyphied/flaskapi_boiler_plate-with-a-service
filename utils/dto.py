from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('user', description='user realted opertaions')
    user = api.model('user', {
                'email': fields.String(required=True, description='user email address'),
                'password': fields.String(required=True, description='user password')

    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class CarServiceDto:
    api = Namespace('car service', description='car service prediction model')
    car_service = api.model('car service',{
        'car_model': fields.String(required=True, description= 'The car Model')
    })