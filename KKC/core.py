from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.secret_key = "patate"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from KKC.model import Block

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#block = Block("sdadafqfqw21", "12312441")

#db.session.add(block)
db.session.commit()

admin = Admin(app, name='Lil Big Boi', template_mode='bootstrap3')

from KKC.routes import *

