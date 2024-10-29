from flask import Blueprint, request, render_template, redirect, url_for, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from .models import User
from myapp import db, csrf  # Ensure CSRF is imported
from flask_wtf.csrf import generate_csrf, CSRFProtect, CSRFError  # Import generate_csrf for token generation

csrf = CSRFProtect()
main = Blueprint('main', __name__)

# Sample data for demonstration
sample_data = [
    {"id": 1, 'name': 'Geo Osama', 'email': 'geosama@gmail.com', 'sex': 'Male', 'age': 21},
    {"id": 2, 'name': 'Rainy Blu', 'email': 'rainyblu@yahoo.com', 'sex': 'Female', 'age': 30}
]

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # Dummy user credentials for demonstration
        if username == "admin" and password == "test123":
            access_token = create_access_token(identity=username)
            response = make_response(redirect(url_for('main.home')))  # Redirect to home
            set_access_cookies(response, access_token)  # Set the access token as a cookie
            return response

        error = "Invalid username or password. Please try again."
        return render_template('login.html', error=error, csrf_token=generate_csrf())

    return render_template('login.html', csrf_token=generate_csrf())


@main.route('/home')
@jwt_required()
def home():
    return render_template('index.html')


@main.route('/view_data')
@jwt_required()
def view_data():
    return render_template('viewAllData.html', data=sample_data)

@main.route('/add_data', methods=['GET', 'POST'])
@jwt_required()
def add_data():
    current_user = get_jwt_identity()  # Get the current user's identity
    print(f"Current User: {current_user}")  # Debugging statement

    if request.method == 'POST':
        # Check CSRF token if necessary, depending on your setup
        print(f"Form data received: {request.form}")  # Debugging statement

        new_entry = {
            'id': len(sample_data) + 1,  # Auto-incrementing ID for sample data
            'name': request.form['name'],
            'email': request.form['email'],
            'sex': request.form['sex'],
            'age': int(request.form['age'])
        }
        sample_data.append(new_entry)
        return redirect(url_for('main.home'))

    return render_template('addData.html')


@main.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({"error": "CSRF token is invalid.", "message": e.description}), 400

@main.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    current_user = get_jwt_identity()
    return jsonify({"user": current_user, "data": sample_data}), 200
