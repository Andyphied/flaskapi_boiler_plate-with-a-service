from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from resources.errors import errors

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://car-service-api:car-service-api@car-service-api-db-uzypc.mongodb.net/car-service-api-db?retryWrites=true&w=majority'
}

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run()