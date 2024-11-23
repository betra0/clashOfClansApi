from flask import Blueprint

testRoute = Blueprint('Test', __name__)

@testRoute.route('/', methods=['GET'])
def admin_dashboard():
    return "Welcome to the admin dashboard!"
