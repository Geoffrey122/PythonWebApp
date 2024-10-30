# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# import pyodbc
# from flask_wtf.csrf import CSRFProtect

# db = SQLAlchemy()
# jwt = JWTManager()
# csrf = CSRFProtect()

# def create_app():
#     # Create a Flask application instance
#     app = Flask(__name__)

#     # Configure the database URI with matching credentials
#     app.config['SQLALCHEMY_DATABASE_URI'] = (
#         'mssql+pyodbc://root:admin1234567890@Geoffrey\\SQLEXPRESS/datadb'
#         '?driver=ODBC+Driver+17+for+SQL+Server')
    
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
#     app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
#     app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Read JWT from cookies
#     app.config['WTF_CSRF_ENABLED'] = False

#     db.init_app(app) # Initialize the database and JWT with the app
#     jwt.init_app(app) # Initialize JWTManager
#     csrf = CSRFProtect(app)

#     # Attempt to establish a direct connection using pyodbc
#     server = 'Geoffrey\\SQLEXPRESS'
#     database = 'datadb'
#     username = 'root'
#     password = 'admin1234567890'

#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

#     try:
#         conn = pyodbc.connect(connection_string)
#         print("Database connection established successfully!")
#         conn.close()
#     except pyodbc.Error as e:
#         print("Error connecting to the database:", e)

#     from myapp.routes import main  # Import the blueprint
#     app.register_blueprint(main)

#     with app.app_context():
#         from myapp import models
#         db.create_all()

#     return app

from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Read JWT from cookies
    app.config['WTF_CSRF_ENABLED'] = False

    jwt.init_app(app)  # Initialize JWTManager

    from myapp.routes import main  # Import the blueprint
    app.register_blueprint(main)

    return app