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
def test_fun():
    return "Hello"

# APIs

'''
    Desc : Get the data from the request body in JSON Format
    @json 
    {
        parameter1 : "p1_val"
        parameter2 : "p2_val"    
    }
'''
@app.route('/api-route-1', methods=['GET'])
def register_user():
    data = request.json
    return jsonify(success=True)

# Main
if __name__ == '__main__':
    app.run(debug=True)
