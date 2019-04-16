from deleteLater import Block

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from flask import Flask, session
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from deleteLater.Block import db


app = Flask(__name__)
app.secret_key = "patate"

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Lil Big Block', template_mode='bootstrap3')
data = ["149849198", "28949498498", "39849849841"]
block = Block.Block("1231dwqwe", data)

db.create_all()
db.session.add(block)
admin.add_view(ModelView(Block.Block, db.session))

def encode_key(key):
    return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

@app.route("/status")
def afficherKey():
    priv_key = session["rsa"]
    pk = load_pem_private_key(priv_key, None, default_backend())
    pub_key = pk.public_key()
    return Block.Block.afficher_public_key(Block, pub_key)

@app.route("/load")
def loadKey():
    pk = Block.Block.load_private_key(Block, 'privatekey.txt')
    session['rsa'] = encode_key(pk)
    return "Clé chargée"

@app.route("/")
def hello():
    return "Hello World!"


app.run()