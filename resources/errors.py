class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class NoAuthorizationError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 409
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "NoAuthorizationError": {
         "message": "Unauthorized access. A token is needed to access this feature",
         "status": 401
     }
}