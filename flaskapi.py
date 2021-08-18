import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()