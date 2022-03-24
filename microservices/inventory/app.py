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

# TODO
@app.route('/hospital/<hosp_id>/getall', methods=['POST'])
def get_all_meds(hosp_id):
    disp_id=db.collection('hospital').document(hosp_id).get().to_dict()['dispensary']
    meds=db.collection('dispensary').document(disp_id).get().to_dict()

    # TODO VINAYAK change schema to 
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

    return jsonify(success=True,meds=meds)

# Main
if __name__ == '__main__':
    app.run(debug=True , port = 5000)
