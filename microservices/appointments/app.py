from flask import Flask, json, render_template, jsonify, request, session, flash, redirect, url_for, send_file
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import requests

# Initialization
cred = credentials.Certificate('../../creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
app.secret_key = "SECRET_FROM_ENV_MNO"

# Functions


# APIs

'''
    Desc : Book a new appointment
    @json 
    {
        patient_id : "random_patient_id"
        doctor_id : "random_doctor_id"
        datetime : "some datetime format" (Store as it is in db as of now)
        description : "details about disease"
    }
'''
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    try:
        # store this data (also add status = open) in appointments collection and get appointment id
        data['status'] = "open"
        data['appointment_id'] = data['patient_id'] + "_"+data['doctor_id']+"_"+data['datetime']
        db.collection("appointments").document(
            data['appointment_id']).set(data, merge=True)

        # open patients collection, add this appointment id to appointments array []
        patient_ref = db.collection("patient").document(data['patient_id'])
        patient_ref.update(
            {u'appointments': firestore.ArrayUnion([data['appointment_id']])})

        # open doctors collection, add this appointment id to appointments array []
        doctor_ref = db.collection("doctor").document(data['doctor_id'])
        doctor_ref.update(
            {u'appointments': firestore.ArrayUnion([data['appointment_id']])})

        return jsonify(success=True)
    except:
        return jsonify(success=False)


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
    user_data = db.collection("users").document(data['userid']).get().to_dict()
    # depending on that, fetch the required document from doctor's or patient's collection
    # fetch the appointments array, then return the list of appointments whose status is open as json

    if(user_data['role'] == 0 or user_data['role'] == 1):
        appointments=[]
        if(user_data['role'] == 0):
            appointments = db.collection("patient").document(
                data['userid']).get().to_dict()['appointments']
        else:
            appointments = db.collection("doctor").document(
                data['userid']).get().to_dict()['appointments']

        open_appointments = []
        closed_appointments = []
        for appointment in appointments:
            app_data = db.collection('appointment').document(
                appointment).get().to_dict()
            if app_data['status'] == "open":
                open_appointments.append(app_data)
            else:
                closed_appointments.append(app_data)

        return jsonify(success=True, open_appointments=open_appointments , closed_appointments = closed_appointments)

    else:

        return jsonify(success=False)


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
    # Have to check doctor in main app.py itself
    try:
        # update appointment status as closed and also add the data received
        current_appointment=db.collection('appointment').document(data['appointment_id'])
        current_appointment.set({"description": data["description"], "prescription": data["prescription"],"next_appointment": data["next_appointment"], "status": "closed"}, merge=True)

        current_appointment_data=current_appointment.get().to_dict()
        # if next_appointment is not null, then create a new appointment as a followup for this
        next_appointment_date=current_appointment_data['next_appointment']
        if(next_appointment_date is not NULL):
            new_appointment_id=current_appointment_data['doctor_id']+"_"+current_appointment_data['patient_id']+"_"+next_appointment_date
            
            # db.collection('appointment').document(new_appointment_id)
            # modify /book_appointment route below
            # new_appointment.set({...})
            #??????????????????????
            
            dictToSend = {"appointment_id":new_appointment_id,"doctor_id":current_appointment_data["doctor_id"],"patient_id":current_appointment_data["patient_id"],"datetime":NULL,"description":current_appointment_data["description"]}
            res = requests.post('/book_appointment', json=dictToSend) # NOT TESTED
            print('response from server:',res.text)
            dictFromServer = res.json()
            print(dictFromServer)

        return jsonify(success=True)
    except:
        return jsonify(success=False)

# Main
if __name__ == '__main__':
    app.run(debug=True , port = 5001)
