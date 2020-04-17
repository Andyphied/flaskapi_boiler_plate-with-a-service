from .carservice import CarService
from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(CarService, '/api/carservice')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')