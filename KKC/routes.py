from KKC.core import app
from KKC.action import load_private_key, filenamePrivateKey, afficher_public_key, Portefeuille

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from flask import session

portefeuille = Portefeuille()


def encode_key(key):
    return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )


@app.route("/status")
def afficher_key():
    priv_key = session["rsa"]
    pk = load_pem_private_key(priv_key, None, default_backend())
    pub_key = pk.public_key()
    return afficher_public_key(pub_key)


@app.route("/load")
def load_key():
    session['rsa'] = encode_key(portefeuille.private_key)
    return "Clé chargée"


@app.route("/solde")
def show_balance():
    return "Balance portefeuille : " + str(portefeuille.balance) + " KKC"


@app.route("/")
def hello():
    return "Bonjour"
