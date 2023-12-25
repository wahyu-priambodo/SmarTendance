from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

api = Api(prefix='/api/v1', validate=True, doc='/api/v1/docs', version='1.0', title='SmarTendance REST API Documentations', description='REST API for SmarTendance App')
db = SQLAlchemy()
migrate = Migrate()

cors = CORS()
jwt = JWTManager()