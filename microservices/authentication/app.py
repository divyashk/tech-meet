from flask import Flask, json, render_template, jsonify, request, session, flash, redirect, url_for, send_file
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import re
from passlib.hash import sha256_crypt

# Initialization 
cred = credentials.Certificate('../../creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

def is_user_id_valid(uid):
    # Return True or False depending on if the username is valid or not
    # Does NOT check if the username already exists or 
    # Extra layer of security kind of
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if (regex.search(uid) != None):
        return False
    return True

@app.route('/test', methods=['GET'])
# Functions
def add_patient_to_db(user_id="" , patient_data=""):
    # Add patient_data to patient's collection and also store "user_id"

    if(user_id is not '' and patient_data is not ''):
        db.collection("patient").document(user_id).set(patient_data, merge=True)
        return True
    else:
        return False
    # data={"age":"26","gender":"M","nhid":"_testing","password":"password test","patient_address":"xyz,abc","patient_name":"Mr X","phone_number":"9876543210","username":"_testing"}
    # db.collection("patient").document("_testing").set(data, merge=True)


def add_doctor_to_db(user_id , doctor_data):
    # Add doctor_data to doctor's collection and also store "user_id"
    return True

def add_hospital_to_db(user_id , patient_data):
    # Add hospital_data to hospital's collection and also store "user_id"
    return True

# APIs

'''
    Desc : Create a new account
    @json 
    {
        email : "xyz@gmail.com"
        passwd : "letmein"  
        role(type) : (0 or 1 or 2) [0 --> Patient , 1 --> Doctor , 2 --> Hospital]
        userdata : {object based on role}  
    }
'''
# @app.route('/register', methods=['POST'])
@app.route('/create_account', methods=['POST'])
def register_user():
    '''
    Get the data from the request body in JSON Format
    @json needed
    - password
    - username
    - type
    - Rest any other details like name, etc
    '''
    data = request.json
    # image = data['image']
    # print(image)
    compulsary_items = ["username", "password", "type"]
    # other fields are ["age","gender","nhid","patient_address","patient_name","phone_number"]

    for item in compulsary_items:
        if item not in data:
            return jsonify(success=False, err_code='1', msg=item + 'not passed')

    if (is_user_id_valid(data['username'])):
        # User id is valid, go ahead
        data['password'] = sha256_crypt.encrypt(str(data['password']))

        # Update the user in the database
        db.collection("users").document(data['username']).set(data, merge=True)

        session['logged_in'] = True
        session['username'] = data['username']
        session['type'] = data['type']
        return jsonify(success=True)
    else:
        return jsonify(success=False, err_code='0')

'''
    Desc : Authenticate Login
    @json 
    {
        email : "xyz@gmail.com"
        passwd : "letmein"
    }
'''
# @app.route('/login-check', methods=['POST'])
# def user_login():
    # data = request.json
    
    # return jsonify(success=True , role = 1)
    # if failure
    # return jsonify(success=False)
@app.route('/login', methods=['POST'])
def user_login():
    '''
    The main login page which functions using the apis and all
    '''
    # use email to get user data from user's collection (password and role)
    # hash the password and compare with password
    # if success
    
    # if "logged_in" in session and session["logged_in"]: # handled in app.py itself
    #     return redirect(url_for("profile"))

    data = request.json
    fire_req_data = db.collection("users").document(
        data["username"]).get().to_dict()
    pass_hash = fire_req_data['password']

    if sha256_crypt.verify(data["password"], pass_hash):
        print("Password match successfully, login the user")

        if data["username"] == "root":
            # This is a superuser!!
            session['is_super_user'] = True
            session['super_user_secret'] = "admin@ppd"

        session['logged_in'] = True
        session['username'] = data['username']
        session['type'] = data['type']
        return jsonify(success=True, role = 1)
    else:
        print("Password does not match")
        return jsonify(success=False, err="Password does not match")

# Main
if __name__ == '__main__':
    app.run(debug=True)
