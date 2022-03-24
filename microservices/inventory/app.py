# from asyncio.windows_events import NULL
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
app.secret_key = "SECRET_FROM_ENV_PQR"


# APIs

'''
    Desc : Add item to inventory
    @json 
    {
        med: {
            id : "some unique"  
            item_name : "paracetemol",
            quantity : 10,
            price : "Rs 100" 
        },
        dispensary: "name"
    }
'''
@app.route('/add', methods=['POST'])
def add_item_to_inv():
    data = request.json
    # Add item to inventory for a particular dispensary
    db.collection('dispensary').document(data['dispensary']).update(
            {u'meds': firestore.ArrayUnion([data['med']])})

    return True

'''
    Desc : 
    @json 
    {
        
        id : "some unique" ,
        field_to_change : "field", 
        value : "value",
        dispensary: "name",
    }
'''
@app.route('/update', methods=['PATCH'])
def update_item_from_inv():
    data = request.json
    # Update an item in inventory for a particular dispensary ( for adjusting price, quantity, etc) 
    med=db.collection('dispensary').document(data['dispensary']).where(u'medId', u'==',data['id'])
    new_data={}
    if("price" in data):
        new_data['price']=data['price']
    if("quantity" in data):
        new_data['quantity']=data['quantity']
    med.set(new_data,merge=True)

    return True

'''
    Desc : Add item to inventory
    @json 
    {
        id : "some unique" ,
        dispensary: "name"
    }
'''
@app.route('/fetch/<dispensary>/<item_name>', methods=['GET'])
def fetch_item_from_inv(dispensary,item_name):
    # data = request.json
    # Search for an item in inventory and return
    item=db.collection('dispensary').document(dispensary).where(u'medId', u'==',item_name).get().to_dict()
    return jsonify(success=True,item=item)

@app.route('/hospital/<hosp_id>/getall', methods=['POST'])
def get_all_hospital_meds(hosp_id):
    try:
        disp_id=db.collection('hospital').document(hosp_id).get().to_dict()['dispensary'][0]
        allMedsData=db.collection('dispensary').document(disp_id).get().to_dict()
        return jsonify(success=True,allMedsData=allMedsData)
    except:
        return jsonify(success=False)

@app.route('/doctor/<doctor_id>', methods=['GET'])#POST
def get_doctor_slots(doctor_id):
    try:
        doctor_details=db.collection('doctor').document(doctor_id).get().to_dict()
        slots={}
        try:
            refs = db.collection('doctor').document(doctor_id).collection('slots').stream()
            for ref in refs:
                slots[ref.id]=ref.to_dict()
        except:
            refs={}
        
        allDoctorData={"doctor_details":doctor_details,"slots":slots}
        print(allDoctorData)
        return jsonify(success=True,allDoctorData=allDoctorData)
    except:
        return jsonify(success=False)

@app.route('/medicines' , methods = ['GET'])
def get_all_meds():
    refs = db.collection('medicine').stream()
    allMedsData = {}
    for ref in refs:
        allMedsData[ref.id] = ref.to_dict()
    return allMedsData

# Main
if __name__ == '__main__':
    app.run(debug=True , port = 5000)
