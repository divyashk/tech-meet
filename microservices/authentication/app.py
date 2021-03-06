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
app.secret_key = "SECRET_FROM_ENV_ABC"

# Functions
def add_patient_to_db(user_id="" , patient_data=""):
    # Add patient_data to patient's collection and also store "user_id"

    if(user_id != '' and patient_data != ''):
        db.collection("patient").document(user_id).set(patient_data, merge=True)
        return True
    else:
        return False

def add_doctor_to_db(user_id ="", doctor_data=""):
    # Add doctor_data to doctor's collection and also store "user_id"
    if(user_id != '' and doctor_data != ''):
        db.collection("doctor").document(user_id).set(doctor_data, merge=True)
        return True
    else:
        return False

def add_hospital_to_db(user_id ="", hospital_data=""):
    # Add hospital_data to hospital's collection and also store "user_id"
    if(user_id != '' and hospital_data != ''):
        db.collection("hospital").document(user_id).set(hospital_data, merge=True)
        return True
    else:
        return False

def is_user_id_valid(uid):
    # Return True or False depending on if the username is valid or not
    # Does NOT check if the username already exists or 
    # Extra layer of security kind of
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if (regex.search(uid) != None):
        return False
    return True

# APIs

'''
    Desc : Create a new account
    @json 
    {
        email : "xyz@gmail.com"
        passwd : "letmein"  
        role : (0 or 1 or 2) [0 --> Patient , 1 --> Doctor , 2 --> Hospital]
        userdata : {object based on role}  
    }
'''
@app.route('/create_account', methods=['POST'])
def register_user():
    '''
    Get the data from the request body in JSON Format
    @json needed
    - password
    - username
    - role
    - Rest any other details like name, etc
    '''
    data = request.json
    print(data)
    compulsary_items = ["username", "password", "role"] # username and email are same

    for item in compulsary_items:
        if item not in data:
            return jsonify(success=False, err_code='1', msg=item + 'not passed')

    if (is_user_id_valid(data['username'])):
        # User id is valid, go ahead
        data['password'] = sha256_crypt.encrypt(str(data['password']))

        # Update the user in the database
        db.collection("users").document(data['username']).set({"username":data["username"], "password":data["password"], "role":data["role"]}, merge=True)

        # session['logged_in'] = True
        # session['username'] = data['username']
        # session['type'] = data['type']
        # session['role'] = data['role']

        if(data['role']==0):
            add_patient_to_db(data['username'],data['userdata'])

        if(data['role']==1):
            add_doctor_to_db(data['username'],data['userdata'])

        if(data['role']==2):
            add_hospital_to_db(data['username'],data['userdata'])


        return jsonify(success=True)
    else:
        return jsonify(success=False, err_code='0')

@app.route('/login', methods=['POST']) # TESTED
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

        # if data["username"] == "root":
        #     # This is a superuser!!
        #     session['is_super_user'] = True
        #     session['super_user_secret'] = "admin@ppd"

        return jsonify(success=True, role = fire_req_data['role'])
    else:
        print("Password does not match")
        return jsonify(success=False, err="Password does not match")

@app.route('/username', methods=['POST']) # TESTED
def check_if_username_exists():
    # needs username and check if the username exists or not
    # returns true and false depending on if it exists
    # also pass type in the parameters now
    req_data = request.json
    if is_user_id_valid(req_data["username"]):
        userid_ref = db.collection("users").document(
            req_data['username']).get()

        if userid_ref.exists:
            print("username exists")
            if "image" in userid_ref.to_dict():
                return jsonify(success=True , image=userid_ref.to_dict()["image"])
            else:
                return jsonify(success=True, image="")
        else:
            print("username doesn't exists")
            return jsonify(success=False, err_code='1')

    else:
        return jsonify(success=False, err_code='0')

# Main
if __name__ == '__main__':
    app.run(debug=True , port = 5000)
