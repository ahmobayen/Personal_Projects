<<<<<<< HEAD
# application/api/__init__.py

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swagger = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API application"})


=======
# application/api/__init__.py

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swagger = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API application"})


>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
