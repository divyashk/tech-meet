from flask import Flask, json, render_template, jsonify, request, session, flash, redirect, url_for, send_file
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Initialization 
cred = credentials.Certificate('creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# APIs
'''
    Desc : get all the details about a room
    @json 
    {
        hospital_id : "value",
        room_no: "value"
    }
'''
# @app.route('/get_room_details', methods=['GET'])
# def get_room_info():
#     data = request.json
#     # fetch all the information stored about a room from the database
#     return True

'''
    Desc : allocate a room
    @json 
    {
        hospital_id : "value",
        room_no: "value",
        patient_id : "value"
    }
'''
@app.route('/allocate_room', methods=['POST'])
def allocate_room():
    data = request.json
    # allocate an empty room to a patient and store in the database accordingly
    return True

'''
    Desc : 
    @json 
    {
        hospital_id : "value",
        room_no: "value"
    }
'''
@app.route('/free_room', methods=['POST'])
def get_room_info():
    data = request.json
    # free a particular room
    return True


# Main
if __name__ == '__main__':
    app.run(debug=True,  threaded=True , port = 5000)
