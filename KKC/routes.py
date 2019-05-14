from KKC.core import app
from KKC.action import load_private_key, filenamePrivateKey, afficher_public_key
from KKC.model import Portefeuille, Transaction
from KKC.templates.forms import TransactionForm

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from flask import session, render_template, request, flash, redirect

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


@app.route("/solde")
def show_balance():
    return "Balance portefeuille : " + str(portefeuille.balance) + " KKC"


@app.route("/transaction", methods=["POST", "GET"])
def transferer():
    form = TransactionForm()
    if request.method == 'POST':

        Transaction.creer_transaction(Transaction.self, form.destinataire, form.montant)
        return redirect('/')
    return render_template("transaction.html", title='Nouvelle transaction', form=form)


@app.route("/")
def hello():
    session['rsa'] = encode_key(portefeuille.private_key)
    html = "<h1>Bonjour</h1>" + "<li> <a href='/solde'>Charger le solde</a></li>" \
                                "<li> <a href='/status'>Afficher la clé publique</a></li>"\
                                "<li> <a href='/transaction'>Transaction</a></li>"\
                                "<li> <a href='/admin'>Admin</a></li>"
    return html
