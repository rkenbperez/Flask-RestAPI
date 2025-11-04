from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
def home():
    return "<h1>Welcome to the Home Page</h1>"