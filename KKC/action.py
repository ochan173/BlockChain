
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

import urllib.request, json

#from KKC.model import Block

filenamePrivateKey = 'privatekey.txt'


def preuve_de_travail(Block):

    PreuveString = "{}{}{}{}".format(Block.hashset_precedent, "".join(Block.data), str(Block.date), str(Block.nb_aleatoire))
    HashValide = False
    cpt = 0
    DebutValide = "00000"
    HashPreuve = hashlib.sha256(PreuveString.encode()).hexdigest()

    while not HashValide:
        if (DebutValide == HashPreuve[:5]):
            HashValide = True
        else:
            cpt += 1
            HashPreuve = hashlib.sha256(HashPreuve.encode()).hexdigest()

    Block.NbPreuves = cpt
    return HashPreuve


def hash_message(p_message):
    hashed = hashlib.sha256(p_message.encode()).hexdigest()
    print(hashed)


def gen_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    return private_key


def load_public_key():
    private_key = load_private_key(filenamePrivateKey)
    public_key = private_key.public_key()
    pub_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pub_key


def afficher_public_key(key):
    return key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)


def save_key(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


def load_private_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key




