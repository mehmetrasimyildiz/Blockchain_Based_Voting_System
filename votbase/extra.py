import base64
import os
import random

import requests
from twilio.rest import Client
from .models import Vote_Auth
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def sms(tonum, data):
    accunt_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')

    client = Client(accunt_sid, auth_token)
    client.messages.create(from_=os.environ.get('ACCOUNT_NUMBER'), to=tonum, body=data)


def get_vote_auth():
    vote_auth = Vote_Auth.objects.all()
    return vote_auth


def encrypt(password, message1, message2):
    Bmessage1 = message1.encode('ASCII')
    Bmessage2 = message2.encode('ASCII')
    Bpassword = password.encode('ASCII')
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000)
    key = base64.urlsafe_b64encode(kdf.derive(Bpassword))

    f = Fernet(key)
    token1 = f.encrypt(Bmessage1)
    token2 = f.encrypt(Bmessage2)

    return token1.decode('ASCII'), token2.decode('ASCII'), base64.b64decode(salt).decode('ASCII')


def decrypt(password, token1, token2, salt):
    Bpassword = password.encode('ASCII')
    bToken1 = token1.decode('ASCII')
    bToken2 = token2.decode('ASCII')
    enSalt = salt.encode('ASCII')
    bSalt = base64.b64decode('ASCII')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bSalt,
        iterations=480000)
    key = base64.urlsafe_b64encode(kdf.derive(Bpassword))
    f = Fernet(key)
    token1 = f.decrypt(bToken1)
    token2 = f.decrypt(bToken2)
    return token1.decode('ASCII'), token2.decode('ASCII')

#def keyGen():
#  keyPair = RSA.generate(bits=1024)
#  return keyPair.d,keyPair.n,keyPair.e


def passPhrase():
    length = random.randint(5, 20)
    API_KEY = os.getenv("API_NİNJA_API")
    api_url = 'https://api.api.ninjas.com/v1/passwordgenerator?length={}'.format(length)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data['random_password']
    else:
        print("Error:", response.status_code, response.text)
