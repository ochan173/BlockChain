from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class BD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashPrecedent = db.Column(db.String(100), unique=True, nullable=False)
    data = db.Column(db.String(100), unique=False, nullable=False)
    nbPreuve = db.Column(db.Integer, unique=False, nullable=False)
    nbAleatoire = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    hashPreuve = db.Column(db.String(100), unique=False, nullable=False)