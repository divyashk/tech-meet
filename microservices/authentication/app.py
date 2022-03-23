from flask import Flask, json, render_template, jsonify, request, session, flash, redirect, url_for, send_file
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Initialization 
cred = credentials.Certificate('../../creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Functions
def add_patient_to_db(user_id , patient_data):
    # Add patient_data to patient's collection and also store "user_id"
    return True

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
        role : (0 or 1 or 2) [0 --> Patient , 1 --> Doctor , 2 --> Hospital]
        userdata : {object based on role}  
    }
'''
@app.route('/create_account', methods=['POST'])
def register_user():
    data = request.json
    # hash the password
    # store email , passwd and role to users collection, and get object id
    # based on the value of role, call add_{patient , doctor , hospital}_to_db
    return jsonify(success=True)


'''
    Desc : Authenticate Login
    @json 
    {
        email : "xyz@gmail.com"
        passwd : "letmein"
    }
'''
@app.route('/login-check', methods=['POST'])
def user_login():
    data = request.json
    # use email to get user data from user's collection (password and role)
    # hash the password and compare with password
    # if success
    return jsonify(success=True , role = 1)
    # if failure
    return jsonify(success=False)

# Main
if __name__ == '__main__':
    app.run(debug=True)
