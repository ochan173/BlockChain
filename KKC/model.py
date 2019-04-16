from KKC.action import preuve_de_travail
from KKC.core import db

import random
import datetime


class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashPrecedent = db.Column(db.String(100), unique=True, nullable=False)
    data = db.Column(db.String(100), unique=False, nullable=False)
    nbPreuve = db.Column(db.Integer, unique=False, nullable=False)
    nbAleatoire = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    hashPreuve = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, hashsetPrecedent, data):
        self.HashsetPrecedent = hashsetPrecedent
        self.Data = data
        self.NbPreuves = 0
        self.NbAleatoire = random.randint(1, 1000000)
        self.Date = datetime.time
        self.HashPreuve = preuve_de_travail(self)
