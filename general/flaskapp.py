from flask_cors import CORS
from flask import Flask,render_template,request,jsonify

app = Flask(__name__, template_folder='../frontend/static/html',static_folder='../frontend/static')
CORS(app)