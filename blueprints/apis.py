from . import blueprint
from flask import request, session
import requests

appointments_ms = "http://127.0.0.1:5001"
authentication_ms = "http://127.0.0.1:5002"
infra_ms = "http://127.0.0.1:5003"
inventory_ms = "http://127.0.0.1:5004"

""" Appointments Microservice APIs """

@blueprint.route("/appointments/book_appointment", methods=['POST'])
def book_appointment():
  data = request.json
  url = appointments_ms + '/book_appointment'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/appointments/show_appointments", methods=['POST'])
def show_appointment():
  data = request.json
  url = appointments_ms + '/show_appointments'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/appointments/close_appointment", methods=['POST'])
def close_appointment():
  data = request.json
  print(data)
  url = appointments_ms + '/close_appointment'
  x = requests.post(url, json = data)
  return x.json()

""" Authentication Microservice APIs """

@blueprint.route("/authentication/username", methods=['POST'])
def check_username():
  print("Check username exists are left")
  data = request.json
  url = authentication_ms + '/username'
  x = requests.post(url, json = data)
  return x.json()


@blueprint.route("/authentication/create_account", methods=['POST'])
def create_account():
  data = request.json
  url = authentication_ms + '/create_account'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/authentication/login", methods=['POST'])
def login():
  data = request.json
  url = authentication_ms + '/login'
  x = requests.post(url, json = data)
  session.update(x.json()['session'])
  return x.json()


""" Infrastructure Microservice APIs """

@blueprint.route("/infra/get_room_details", methods=['POST'])
def get_room_details():
  data = request.json
  url = infra_ms + '/get_room_details'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/infra/allocate_room", methods=['POST'])
def allocate_room():
  data = request.json
  url = infra_ms + '/allocate_room'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/infra/free_room", methods=['POST'])
def free_room():
  data = request.json
  url = infra_ms + '/free_room'
  x = requests.post(url, json = data)
  return x.json()


""" Inventory Microservice APIs """

@blueprint.route("/inventory/add", methods=['POST'])
def add():
  data = request.json
  url = inventory_ms + '/add'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/inventory/update", methods=['PATCH'])
def update():
  data = request.json
  url = inventory_ms + '/update'
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/inventory/fetch/:item_name", methods=['GET'])
def fetch(item_name):
  data = request.json
  url = inventory_ms + '/fetch/' + item_name
  x = requests.post(url, json = data)
  return x.json()

@blueprint.route("/inventory/hospital/:hosp_id/getall", methods=['POST'])
def get_all(hosp_id):
  data = request.json
  url = inventory_ms + '/hospital/' + hosp_id + "/getall"
  x = requests.post(url, json = data)
  return x.json()
