#%%
import pandas as pd
import json

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

doctor_detail.head()

#%%
hospital_detail.head()

#%%
hosp_dict = {}
# first create a dictionary of hospital
for index, row in hospital_detail.iterrows():
    hosp_dict[row['hospital_name']] = row['username']

hosp_dict
#%%

doct_dict = {}
# we want to add hospital_id to the doctor details
for index, row in doctor_detail.iterrows():
    hospital = row['hospital']

    if hospital in doct_dict:
        doct_dict[hospital].append(row['doctor_name'])
    else:
        doct_dict[hospital] = [row['doctor_name']]

    # row['hospital_id'] = hosp_dict[hospital]
    # print(row['hospital_id'])

doct_dict

#%%
mp1 = []; mp2 = []
for key in doct_dict:
    mp1.append(key)

for key in hosp_dict:
    mp2.append(key)

hops_doct_dict = {}
for i in range(len(mp1)):
    hops_doct_dict[mp1[i]] = mp2[i]

hops_doct_dict

#%% Finally adding hospital id in doctor_detail
hospital_usernames = []
for index, row in doctor_detail.iterrows():
    hospital = row['hospital']

    hospital_usernames.append(hosp_dict[hops_doct_dict[hospital]])

doctor_detail['hospital_username'] = hospital_usernames
doctor_detail
#%% Add a list of doctors in hospital, for that keep a list of data

doct_username_dict = {}
for index, row in doctor_detail.iterrows():
    hospital_username = row['hospital_username']

    if hospital_username in doct_username_dict:
        doct_username_dict[hospital_username].append(row['username'])
    else:
        doct_username_dict[hospital_username] = [row['username']]

doctors_usernames = []
for index, row in hospital_detail.iterrows():
    doctors_usernames.append(doct_username_dict[row['username']])

hospital_detail['doctors_username'] = doctors_usernames
hospital_detail

#%% We have 11 hospitals for now, so we have one dispensary for each
dispensary = [
    ["dispId1"],
    ["dispId2"],
    ["dispId3"],
    ["dispId4"],
    ["dispId5"],
    ["dispId6"],
    ["dispId1"],
    ["dispId2"],
    ["dispId3"],
    ["dispId4"],
    ["dispId5"],
]

hospital_detail['dispensary'] = dispensary
hospital_detail
#%%
print(hospital_detail)

# users_detail = []
# for index, row in hospital_detail.iterrows():
#     data = {
#         "name": row['hospital_name'],
#         "phone": row['phone_no'],
#         "username": row['username'],
#         "password": str(sha256_crypt.encrypt(row['password'])),
#         "role": 2
#     }

#     users_detail.append(data)


# for index, row in doctor_detail.iterrows():
#     data = {
#         "name": row['doctor_name'],
#         "phone": row['phone_no'],
#         "username": row['username'],
#         "password": str(sha256_crypt.encrypt(row['password'])),
#         "role": 1
#     }

#     users_detail.append(data)


# for index, row in patient_detail.iterrows():
#     data = {
#         "name": row['patient_name'],
#         "phone": row['phone_number'],
#         "username": row['username'],
#         "password": str(sha256_crypt.encrypt(row['password'])),
#         "role": 0
#     }

#     users_detail.append(data)

# users_detail
#%%
# for row in users_detail:
#     db.collection('users').document(str(row['username'])).set(row, merge=True)
#     print("Added ", data)

#%% Adding dispensay and medicines data

# dispensary_file = open('dispensary.json')
# dispensary_detail = json.load(dispensary_file)
# dispensary_detail

# for key in dispensary_detail:
#     db.collection('dispensary').document(str(key)).set(dispensary_detail[key], merge=True)
#     print("Added ", key)

# medicine_file = open('medicine.json')
# medicine_detail = json.load(medicine_file)
# medicine_detail

# for key in medicine_detail:
#     db.collection('medicine').document(str(key)).set(medicine_detail[key], merge=True)
#     print("Added ", key)


#%% Add hospital detail in firestore database
# for index, row in hospital_detail.iterrows():
#     # print(row["username"])
#     data = {
#         "hospital_name": row['hospital_name'],
#         "address": row['address'],
#         "phone_no": row['phone_no'],
#         "hospital_rating": row['hospital_rating'],
#         "username": row['username'],
#         "dispensary": row['dispensary'],
#         "password": str(sha256_crypt.encrypt(row['password'])),
#         "doctors_username": row['doctors_username']
#     }

#     db.collection('hospital').document(str(row['username'])).set(data, merge=True)
#     print("Added ", data)

#%%
# Adding doctor_detail to the firestore database
# for index, row in doctor_detail.iterrows():
#     # print(row["username"])
#     data = {
#         "doctor_name": row['doctor_name'],
#         "degree": row['degree'],
#         "medical_profession": row['medical_profession'],
#         "year_of_xp": row['year_of_xp'],
#         "hospital": row['hospital'],
#         "phone_no": row['phone_no'],
#         "username": row['username'],
#         "password": str(sha256_crypt.encrypt(row['password'])),
#         "hospital_username": row['hospital_username']
#     }

#     db.collection('doctor').document(str(row['username'])).set(data, merge=True)
#     print("Added ", data)

#%% Adding patient detail to the firestore
# db.collection('patient') Run only once

# for index, row in patient_detail.iterrows():
#     # print(row["username"])
#     data = {
#         "patient_name": row['patient_name'],
#         "nhid": row['nhid'],
#         "gender": row['gender'],
#         "age": row['age'],
#         "patient_address": row['patient_address'],
#         "phone_number": row['phone_number'],
#         "username": row['username'],
#         "password": str(sha256_crypt.encrypt(row['password']))
#     }

#     db.collection('patient').document(str(row['username'])).set(data, merge=True)
#     print("Added ", data)

# %% appointments
fapnt = open('appointment.json')
appointment_detail = json.load(fapnt)
# print(appointment_detail)

for key in appointment_detail:
    db.collection('appointment').document(str(key)).set(appointment_detail[key], merge=True)
    print("Added ", key)
