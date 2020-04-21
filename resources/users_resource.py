from flask import request

from database.models import UserSchema
from flask_restplus import Resource
from utils.dto import UserDto
from marshmallow import ValidationError
from service.user_service import save_new_user, get_a_user, get_all_users



users_schema = UserSchema(many=True)
user_schema = UserSchema()

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

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



@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user