from KKC.action import preuve_de_travail
from KKC.core import db
from KKC.action import load_private_key, load_public_key, filenamePrivateKey

import random
import datetime


class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_precedent = db.Column(db.String(100), unique=True, nullable=False)
    data = db.Column(db.String(100), unique=False, nullable=False)
    nb_preuve = db.Column(db.Integer, unique=False, nullable=False)
    nb_aleatoire = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    hash_preuve = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, p_hashset_precedent, p_data):
        self.hashset_precedent = p_hashset_precedent
        self.data = p_data
        self.nb_preuves = 0
        self.nb_aleatoire = random.randint(1, 255)
        self.date = datetime.time
        self.hash_preuve = preuve_de_travail(self)
        self.nb_iterations = 1



