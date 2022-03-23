#%%
import pandas as pd

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from passlib.hash import sha256_crypt

#%% Initialise app

cred = credentials.Certificate('../creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


#%%
doctor_detail = pd.read_csv("doctor_details.csv")
doctor_detail

# %%
hospital_detail = pd.read_csv("hospital_data.csv")
hospital_detail

# %%
patient_detail = pd.read_csv("patient_details.csv")
patient_detail
# %%
# Adding doctor_detail to the firestore database

#%% Adding patient detail to the firestore
# db.collection('patient')

for index, row in patient_detail.iterrows():
    data = {
        "patient_name": row['patient_name'],
        "nhid": row['nhid'],
        "gender": row['gender'],
        "age": row['age'],
        "patient_address": row['patient_address'],
        "phone_number": row['phone_number'],
        "username": row['username'],
        "password": sha256_crypt.encrypt(row['password'])
    }

    db.collection('patient').document(row['username']).set(data, merge=True)
    print("Added ", data)

# %%
