import random
import datetime
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


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
        self.HashPreuve = self.preuve_de_travail()

    def preuve_de_travail(self):
        PreuveString = "{}{}{}{}".format(self.HashsetPrecedent, "".join(self.Data), str(self.Date), str(self.NbAleatoire))
        hashValide = False
        cpt = 0
        debutValide = "00000"
        HashPreuve = hashlib.sha256(PreuveString.encode()).hexdigest()

        while not hashValide:
            if (debutValide == HashPreuve[:5]):
                hashValide = True
            else:
                cpt += 1
                HashPreuve = hashlib.sha256(HashPreuve.encode()).hexdigest()

        self.NbPreuves = cpt
        return HashPreuve

    def hash_message(self, p_message):
        hashed = hashlib.sha256(p_message.encode()).hexdigest()
        print(hashed)

    def gen_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        return private_key

    def load_public_key(selfs):
        privateKey = Block.load_private_key(Block, filenamePrivateKey)
        public_key = privateKey.public_key()
        pubKey = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return pubKey


    def afficher_public_key(self, key):
        return key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def save_key(self, pk, filename):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as pem_out:
            pem_out.write(pem)

    def load_private_key(self, filename):
        with open(filename, 'rb') as pem_in:
            pemlines = pem_in.read()
        private_key = load_pem_private_key(pemlines, None, default_backend())
        return private_key


filenamePrivateKey = 'privatekey.txt'

#pk = Block.load_key(Block, filenamePrivateKey)
#public_key = pk.public_key()

message = b"allo"

#signer en hex
#signature = pk.sign(message,
#    padding.PSS(
#       mgf=padding.MGF1(hashes.SHA256()),
#        salt_length=padding.PSS.MAX_LENGTH
#    ),
#   hashes.SHA256())


#public_key.verify(signature,
#    message,
#    padding.PSS(
#    mgf=padding.MGF1(hashes.SHA256()),
#    salt_length=padding.PSS.MAX_LENGTH),
#    hashes.SHA256())


#print(signature)

#pk = Block.load_key(Block, 'key.txt')
#message = input()
#Block.hash_messag(Block, message)

#data = ["149849198", "28949498498", "39849849841"]
#block = Block("1231dwqwe", data)
#print(block.HashPreuve)
#print(block.NbPreuves)