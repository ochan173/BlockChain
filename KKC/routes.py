from KKC.model import Block
from KKC.core import app

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from flask import session

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
    return Block.afficher_public_key(Block, pub_key)

@app.route("/load")
def loadKey():
    pk = Block.Block.load_private_key(Block, 'privatekey.txt')
    session['rsa'] = encode_key(pk)
    return "Clé chargée"

@app.route("/")
def hello():
    return "Hello World!"