from flask import request

from database.models import User, UserSchema
from flask_restplus import Resource
from utils.dto import UserDto, AuthDto
from marshmallow import ValidationError
from service.user_service import save_new_user
from service.auth_helper import Auth


users_schema = UserSchema(many=True)
user_schema = UserSchema()

api = UserDto.api
_user = UserDto.user

api_auth = AuthDto.api
_user_auth = AuthDto.user_auth

@api.route('/')
class SignupApi(Resource):

    @api.response(201, 'User sucessfully created')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.get_json()
        try:
            data = user_schema.load(data)
        except ValidationError as err:
             err.messages
        return save_new_user(data=data)
        
        
@api_auth.route('/login')
class LoginApi(Resource):

    @api_auth.doc('user login')
    @api_auth.expect(_user_auth, validate=True)
    def post(self):
        data = request.get_json()
        try:
            data = user_schema.load(data)
        except ValidationError as err:
             err.messages
        return Auth.login_user(data=data)