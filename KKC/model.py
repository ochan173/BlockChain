import hashlib

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from KKC.action import load_private_key, filenamePrivateKey, hash_message, load_public_key
from KKC.core import db
from enum import Enum
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import urllib.request, json

class EtatBlock(Enum):
    NOUVEAU = 1
    VALIDATION = 2
    POW_TROUVE = 3
    OK = 4


class EtatTransaction(Enum):
    VALIDE = 1
    INVALIDE = 0


class Block(db.Model):
    __tablename__ = 'block'
    id = db.Column(db.Integer, primary_key=True)
    data = relationship("Transaction", back_populates='block')
    contributeurs = relationship("Contributeur", back_populates='block')
    hash_precedent = db.Column(db.String(100), unique=True, nullable=True)
    nb_preuve = db.Column(db.String(10), unique=False, nullable=True)
    nb_aleatoire = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.String(30), unique=False, nullable=False)
    hash_preuve = db.Column(db.String(100), unique=False, nullable=False)
    premier_confirmateur = db.Column(db.String(500), unique=False, nullable=True)
    hashBlock = db.Column(db.String(100), unique=False, nullable=True)

    def __init__(self, p_hashset_precedent, p_nb_preuves, p_nb_aleatoire, p_date, p_hash_preuve, p_etat
                 , p_premier_confirmateur, p_hash_block):
        self.hashset_precedent = p_hashset_precedent
        self.nb_preuves = p_nb_preuves
        self.nb_aleatoire = p_nb_aleatoire
        self.date = p_date
        self.hash_preuve = p_hash_preuve
        self.etat = p_etat
        self.premier_confirmateur = p_premier_confirmateur
        self.hashBlock = p_hash_block


def get_data():
    with urllib.request.urlopen("https://test.fanslab.io/blockchain") as url:
        data = json.loads(url.read().decode())

        for b in data["KKC"]:
            block = Block(b["previous_hash"], b["proof_number"], int(b["random_number"]),
                b["timestamp"], b["hash_proof"], b["state"], b["proof_finder_identity"], b["hash"])

            if (b["state"] == "OK"):
                db.session.add(block)

                for t in b["datas"]:
                    trans = Transaction(t["sender_address"], t["receiver_address"], t["amount"], t["signature"], block.id, block)
                for c in b["validators"]:
                    contributeur = Contributeur(c["proof_finder_identity"], c["hash"], block.id, block)
                    db.session.add(contributeur)




class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, ForeignKey('block.id'), nullable=True)
    block = relationship("Block", back_populates="data")
    expediteur = db.Column(db.String(100), unique=False, nullable=False)
    receveur = db.Column(db.String(100), unique=False, nullable=False)
    montant = db.Column(db.Integer, unique=False, nullable=False)
    signature = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, expediteur, receveur, montant, signature, id, block):
        self.expediteur = expediteur
        self.receveur = receveur
        self.montant = montant
        self.signature = signature
        self.block_id = id
        self.block = block

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = load_private_key(filenamePrivateKey)
        message = (str(self.expediteur) + str(self.receveur) + str(self.montant))
        message = hash_message(message)

        signature = private_key.sign(
            message, padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())
        return signature


class Portefeuille:
    def __init__(self):
        self.private_key = load_private_key(filenamePrivateKey)
        self.public_key = load_public_key()
        self.balance = 0


class Contributeur(db.Model):
    __tablename__ = 'contributeur'
    id = db.Column(db.Integer, primary_key=True)
    cle_publique = db.Column(db.String(100), unique=False, nullable=False)
    hash = db.Column(db.String(100), unique=False, nullable=False)
    block_id = db.Column(db.Integer, ForeignKey('block.id'), nullable=True)
    block = relationship("Block", back_populates="contributeurs")

    def __init__(self, cle, hash, id, block):
        self.cle_publique = cle
        self.hash = hash
        self.block_id = id
        self.block = block