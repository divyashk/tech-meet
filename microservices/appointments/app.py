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


# APIs

'''
    Desc : Book a new appointment
    @json 
    {
        patientid : "random_patient_id"
        doctorid : "random_doctor_id"
        datetime : "some datetime format" (Store as it is in db as of now)
        description : "details about disease"
    }
'''
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    # store this data (also add status = open) in appointments collection and get appointment id
    # open patients collection, add this appointment id to appointments array []
    # open doctors collection, add this appointment id to appointments array []
    return jsonify(success=True)

'''
    Desc : List all appointments
    @json 
    {
        userid : "random_user_id"
    }
'''
@app.route('/show_appointments', methods=['POST'])
def show_appointments():
    data = request.json
    # fetch the user data from user's collection and identify whether doctor or patient
    # depending on that, fetch the required document from doctor's or patient's collection
    # fetch the appointments array, then return the list of appointments whose status is open as json
    return jsonify(success=True)


'''
    Desc : Close an appointment (Called by a doctor only)
    @json 
    {
        appointment_id : "random_id"
        description : "random text"
        prescription : [medicineId1 , medicineId2 , medicineId3]
        next_appointment : NULL or datetime
    }
'''
@app.route('/close_appointment', methods=['POST'])
def close_appointment():
    data = request.json
    # update appointment status as closed and also add the data received
    # if next_appointment is not null, then create a new appointment as a followup for this
    return jsonify(success=True)

# Main
if __name__ == '__main__':
    app.run(debug=True)
