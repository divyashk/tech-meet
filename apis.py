from flask import Blueprint
apis = Blueprint('apis' , __name__)

@apis.route('/xyz')
def xyz():
    return "Hello"