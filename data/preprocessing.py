#%%
import pandas as pd


#%%
doctor_detail = pd.read_csv("doctor_details.csv")
doctor_detail

# %%
hospital_detail = pd.read_csv("hospital_data.csv")
hospital_detail

# %%
patient_detail = pd.read_csv("patient_data.csv")
patient_detail
# %%
# Adding doctor_detail to the firestore database
