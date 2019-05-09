import hashlib

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from KKC.action import preuve_de_travail, load_private_key, filenamePrivateKey, hash_message, load_public_key
from KKC.core import db
from enum import Enum
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from collections import namedtuple
import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

import urllib.request, json

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
    contributeurs = relationship("Contributeur", back_populates='block')
    hash_precedent = db.Column(db.String(100), unique=True, nullable=False)
    #data = db.Column(db.String(100), unique=False, nullable=False)
    nb_preuve = db.Column(db.Integer, unique=False, nullable=False)
    nb_aleatoire = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    hash_preuve = db.Column(db.String(100), unique=False, nullable=False)
    adressePremierConfirmateur = db.Column(db.String(500), unique=False, nullable=False)
    hashBlock = db.Column(db.String(100), unique=False, nullable=False)

    # def __init__(self, p_hashset_precedent, p_data):
    #     self.hashset_precedent = p_hashset_precedent
    #     self.data = p_data
    #     self.nb_preuves = 0
    #     self.nb_aleatoire = random.randint(1, 255)
    #     self.date = datetime
    #     self.hash_preuve = preuve_de_travail(self)
    #     self.etat = EtatBlock.NOUVEAU
    #     self.adressePremierConfirmateur = ""
    #     self.hashBlock = ""

    def __init__(self, p_hashset_precedent, p_data, p_nb_preuves, p_nb_aleatoire, p_date, p_hash_preuve, p_etat
                 , p_premier_confirmateur, p_hash_block, p_contributeurs):
        self.hashset_precedent = p_hashset_precedent
        self.data = p_data
        self.nb_preuves = p_nb_preuves
        self.nb_aleatoire = p_nb_aleatoire
        self.date = p_date
        self.hash_preuve = p_hash_preuve
        self.etat = p_etat
        self.adressePremierConfirmateur = p_premier_confirmateur
        self.hashBlock = p_hash_block
        self.contributeurs = p_contributeurs


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


def get_data():
    with urllib.request.urlopen("https://test.fanslab.io/blockchain") as url:
        data = json.loads(url.read().decode())
        list_blocks = []
        for b in data["KKC"]:
            block = Block(b["previous_hash"], b["datas"], int(b["proof_number"]), b["random_number"],
                b["timestamp"], b["hash_proof"], b["state"], b["proof_finder_identity"], b["hash"], b["validators"])
            list_blocks.add(block)
    return list_blocks


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, ForeignKey('block.id'), nullable=True)
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

    def __init__(self, cle, hash):
        self.cle_publique = cle
        self.hash = hash