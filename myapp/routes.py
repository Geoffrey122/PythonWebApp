# from flask import Blueprint, request, render_template, redirect, url_for, jsonify, make_response
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
# from .models import User
# from myapp import db, csrf
# from flask_wtf.csrf import generate_csrf, CSRFProtect, CSRFError 

# csrf = CSRFProtect()
# main = Blueprint('main', __name__)

# # Sample data for demo
# sample_data = [
#     {"id": 1, 'name': 'Geo Osama', 'email': 'geosama@gmail.com', 'sex': 'Male', 'age': 21},
#     {"id": 2, 'name': 'Rainy Blu', 'email': 'rainyblu@yahoo.com', 'sex': 'Female', 'age': 30}
# ]

# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get("username")
#         password = request.form.get("password")

#         # Dummy user credentials
#         if username == "admin" and password == "test123":
#             access_token = create_access_token(identity=username)
#             response = make_response(redirect(url_for('main.home')))  # Redirect to home
#             set_access_cookies(response, access_token)
#             return response

#         error = "Invalid username or password. Please try again."
#         return render_template('login.html', error=error, csrf_token=generate_csrf())

#     return render_template('login.html', csrf_token=generate_csrf())

# @main.route('/home')
# @jwt_required()
# def home():
#     return render_template('index.html')

# @main.route('/view_data')
# @jwt_required()
# def view_data():
#     return render_template('viewAllData.html', data=sample_data)

# @main.route('/add_data', methods=['GET', 'POST'])
# @jwt_required()
# def add_data():
#     current_user = get_jwt_identity()
#     print(f"Current User: {current_user}")

#     if request.method == 'POST':
#         print(f"Form data received: {request.form}")

#         new_entry = {
#             'id': len(sample_data) + 1,  # Auto-incrementing ID for sample data
#             'name': request.form['name'],
#             'email': request.form['email'],
#             'sex': request.form['sex'],
#             'age': int(request.form['age'])
#         }
#         sample_data.append(new_entry)
#         return redirect(url_for('main.home'))

#     return render_template('addData.html')

# @main.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return jsonify({"error": "CSRF token is invalid.", "message": e.description}), 400

# @main.route('/data', methods=['GET'])
# @jwt_required()
# def get_data():
#     current_user = get_jwt_identity()
#     return jsonify({"user": current_user, "data": sample_data}), 200

import csv
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
import os

main = Blueprint('main', __name__)

# Define the file paths
CSV_FILE_PATH = 'datadb.csv'
ADMIN_CREDENTIALS_PATH = 'admins.csv'

# Helper functions to read/write data to CSV
def read_data_from_csv():
    data = []
    try:
        with open(CSV_FILE_PATH, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

def write_data_to_csv(data):
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        fieldnames = ['id', 'name', 'username', 'password', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def check_user_credentials(username, password):
    # Replace this with your actual user credential checking logic
    with open(CSV_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

# Helper functions for admin credentials
def check_admin_credentials(username, password):
    try:
        with open(ADMIN_CREDENTIALS_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    return True
    except FileNotFoundError:
        pass
    return False

def save_admin_credentials(username, password, email):
    with open(ADMIN_CREDENTIALS_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'password', 'email'])
        
        # Write the header if the file is empty
        if os.path.getsize(ADMIN_CREDENTIALS_PATH) == 0:
            writer.writeheader()
        
        # Write the new admin credentials
        writer.writerow({'username': username, 'password': password, 'email': email})

@main.route('/admin_view_all')
@jwt_required()
def admin_view_all():
    admins = []
    try:
        with open(ADMIN_CREDENTIALS_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                admins.append(row)
    except FileNotFoundError:
        pass  # If the file is not found, simply pass an empty list
    
    return render_template('adminViewAll.html', admins=admins)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the user is an admin
        if check_admin_credentials(username, password):
            access_token = create_access_token(identity=username)
            response = make_response(redirect(url_for('main.home')))  # Redirect to index.html for admin
            set_access_cookies(response, access_token)
            return response

        # If not an admin, check for regular user credentials
        if check_user_credentials(username, password):
            access_token = create_access_token(identity=username)
            response = make_response(redirect(url_for('main.user_index')))  # Redirect to user_index.html for user
            set_access_cookies(response, access_token)
            return response

        error = "Invalid username or password. Please try again."
        return render_template('login.html', error=error)

    return render_template('login.html')

@main.route('/user_index')
@jwt_required()
def user_index():
    current_user = get_jwt_identity()
    return render_template('user_index.html', username=current_user)

@main.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template('createAdmin.html', error=error)

        # Save admin credentials if passwords match
        save_admin_credentials(username, password, email)
        success = "Admin account created successfully. You can now log in."
        return render_template('createAdmin.html', success=success)

    return render_template('createAdmin.html')

@main.route('/home')
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return render_template('index.html', username=current_user)

@main.route('/view_data')
@jwt_required()
def view_data():
    data = read_data_from_csv()
    return render_template('viewAllData.html', data=data)

@main.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        data = read_data_from_csv()
        new_entry = {
            'id': len(data) + 1,
            'name': request.form['name'],
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email'],
        }
        
        data.append(new_entry)
        write_data_to_csv(data)
        return redirect(url_for('main.home'))

    return render_template('addData.html')

@main.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    current_user = get_jwt_identity()
    data = read_data_from_csv()
    return jsonify({"user": current_user, "data": data}), 200

@main.route('/logout')
def logout():
    response = make_response(redirect(url_for('main.login')))
    unset_jwt_cookies(response)  # Clear JWT cookies if using Flask-JWT-Extended
    return response