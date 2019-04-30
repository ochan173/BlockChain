import hashlib

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from KKC.action import preuve_de_travail, load_private_key, filenamePrivateKey, hash_message
from KKC.core import db
from enum import Enum
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


import random
from datetime import datetime


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
    hash_precedent = db.Column(db.String(100), unique=True, nullable=False)
    #data = db.Column(db.String(100), unique=False, nullable=False)
    nb_preuve = db.Column(db.Integer, unique=False, nullable=False)
    nb_aleatoire = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    hash_preuve = db.Column(db.String(100), unique=False, nullable=False)
    adressePremierConfirmateur = db.Column(db.String(100), unique=False, nullable=False)
    hashBlock = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, p_hashset_precedent, p_data):
        self.hashset_precedent = p_hashset_precedent
        self.data = p_data
        self.nb_preuves = 0
        self.nb_aleatoire = random.randint(1, 255)
        self.date = datetime
        self.hash_preuve = preuve_de_travail(self)
        self.etat = EtatBlock.NOUVEAU
        self.adressePremierConfirmateur = ""
        self.hashBlock = ""


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, ForeignKey('block.id'))
    block = relationship("Block", back_populates="data")
    expediteur = db.Column(db.String(100), unique=False, nullable=False)
    receveur = db.Column(db.String(100), unique=False, nullable=False)
    montant = db.Column(db.Integer, unique=False, nullable=False)
    signature = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, expediteur, receveur, montant, signature, etat):
        self.expediteur = expediteur
        self.receveur = receveur
        self.montant = montant
        self.signature = signature
        self.etat = etat

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = load_private_key(filenamePrivateKey)
        message = (str(self.expediteur) + str(self.receveur) + str(self.montant))
        message = hash_message(message)
        #message = hashlib.sha256(message).hexdigest()

        signature = private_key.sign(
            message, padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())
        return signature


class Contributeur(db.Model):
    __tablename__ = 'cintributeur'
    id = db.Column(db.Integer, primary_key=True)