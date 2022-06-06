# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "pass that dutch"

DATABASE = 'login_reg_db'