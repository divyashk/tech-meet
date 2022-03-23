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


# APIs

'''
    Desc : Add item to inventory
    @json 
    {
        {
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
    return True


'''
    Desc : Add item to inventory
    @json 
    {
        id : "some unique" ,
        dispensary: "name"
    }
'''
@app.route('/fetch', methods=['GET'])
def fetch_item_from_inv(item_name):
    data = request.json
    # Search for an item in inventory and return
    return True

# Main
if __name__ == '__main__':
    app.run(debug=True)
