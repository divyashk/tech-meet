from flask import Flask, json, render_template, jsonify, request, session, flash, redirect, url_for, send_file
import utility
from werkzeug.utils import secure_filename
from functools import wraps
import os
import time
import math 
import datetime
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from dotenv import load_dotenv
import threading
from passlib.hash import sha256_crypt
import re

"""
Init 
"""
load_dotenv()
cred = credentials.Certificate('creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

"""
Functions
"""
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_register'))
    return wrap

def is_user_id_valid(uid):
    # Return True or False depending on if the username is valid or not
    # Does NOT check if the username already exists or 
    # Extra layer of security kind of

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if (regex.search(uid) != None):
        return False

    return True

def weight(i):
    return 5*max(1 , math.log2(i/3600))

"""
APIs
"""

@app.route('/register', methods=['POST'])
def register_user():
    '''
    Get the data from the request body in JSON Format
    @json needed
    - password
    - username
    - type
    - Rest any other details like name, etc
    '''

    print("Hello")
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
        db.collection(type).document(data['username']).set(data, merge=True)

        session['logged_in'] = True
        session['username'] = data['username']
        session['type'] = data['type']
        return jsonify(success=True)
    else:
        return jsonify(success=False, err_code='0')


@app.route('/user_info', methods=['GET', 'POST'])
@is_logged_in
def user_info():
    type = session['type']
    user_info = db.collection(type).document(session['username']).get()

    if user_info.exists:
        print("User exists")
        resDict = {
            "name": user_info.get('patient_name'),
            "contact": user_info.get('phone_number'),
        }
        return jsonify(success=True, user_info=resDict)
    else:
        print("User doesn't exists")
        return jsonify(success=False, err_code='1')


@app.route("/if_logged_in",methods=["POST"])
def if_logged_in():
    if 'logged_in' in session:
         return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/username_exists', methods=['POST'])
def check_if_username_exists():
    # needs username and check if the username exists or not
    # returns true and false depending on if it exists
    # also pass type in the parameters now

    req_data = request.json

    print("Check if username exists in ", req_data["type"])

    if is_user_id_valid(req_data["username"]):
        userid_ref = db.collection(req_data["type"]).document(
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

"""
Routes
"""
@app.route('/favicon.ico')
def give_favicon():
    return send_file('static/download.png')

@app.route('/')
def home():

    type = "hospital"
    return render_template(type + '/dashboard.html', username="priyam")

    username = ""
    if ("username" in session):
        username = session["username"]
        type = "hospital"
        return render_template(type + '/dashboard.html', username=username)
    else:
        return render_template('index.html', username=username)


@app.route('/patient/login')
def patient_login():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("profile"))

    return render_template('patient/login.html')

@app.route('/doctor/login')
def doctor_login():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("profile"))

    return render_template('doctor/login.html')

@app.route('/hospital/login')
def hospital_login():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("profile"))

    return render_template('hospital/login.html')

@app.route('/hospital/<id>/meds')
def get_all_meds(id):
    allMedsData = [
        {
            "id": "some unique 1",
            "item_name": "paracetemol",
            "quantity": 10,
            "price": "Rs 100"
        },
        {
            "id": "some unique 2",
            "item_name": "Dolo 650",
            "quantity": 7,
            "price": "Rs 50"
        }
    ]

    return jsonify(success=True, allMedsData=allMedsData)


@app.route('/hospital/<id>/doctors')
def get_all_doctors(id):
    allDoctorsData = [
        {
            "username": "doc_username1",
            "doctor_name": "doc NAme",
            "degree": "Desgree",
            "medical_profession": "Helo",
            "phone_no": "9811417932"
        }
    ]

    return jsonify(success=True, allDoctorsData=allDoctorsData)

@app.route('/hospital/<id>/beds')
def get_all_beds(id):
    allBedsData = [
        {
            "hospital_id": "value",
            "room_no": "value",
            "patient_id": "value"
        },
        {
            "hospital_id": "value",
            "room_no": "value",
            "patient_id": "value"
        }
    ]

    return jsonify(success=True, allBedsData=allBedsData)

@app.route('/login', methods=['POST'])
def login_register():
    '''
    The main login page which functions using the apis and all
    '''
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("profile"))

    data = request.json
    fire_req_data = db.collection(data['type']).document(
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
        return jsonify(success=True)
    else:
        print("Password does not match")
        return jsonify(success=False, err="Password does not match")

@app.route('/doctor/me')
@is_logged_in
def profile():
    if session['username']:
        username= session['username']

    return render_template("profile.html", username = username, isMe="yes", loginuser=username)

@app.route('/profile/<id>')
def profile_others(id):
    print("for id", id)

    username = ""
    if 'username' in session:
        username = session['username']

    return render_template("profile.html", username = id, isMe="no", loginuser=username)


@app.route('/logout')
def logout():
    session["logged_in"] = False
    session.clear()
    return redirect(url_for('home'))





"""
Test routes
"""

# @app.route('/testfind')
# def testfind():
#     return render_template('testfind.html')

# @app.route('/testvote')
# def testvote():
#     return render_template('testvote.html')

# @app.route('/testdelete')
# def testdelete():
#     return render_template('testdelete.html')

# @app.route('/testcomment')
# def testcomment():
#     return render_template('testcomment.html')

@app.route('/dashboard')
def dashboard_route():
    hospital_data = {
        "hospital_name": "Hello",
        "address": "My address"
    }

    return render_template('hospital_dashboard.html', hospital_data = hospital_data)

"""
Main 
"""
if __name__ == '__main__':
    app.run(debug=True)
