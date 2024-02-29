# https://www.tutorialspoint.com/python_blockchain/python_blockchain_developing_client.htm
import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections 

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client: 
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
    
    @property 
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format="DER")).decode("ascii")
    

class Transaction:
    # sender _public_key
    # receiver _public_key
    # transaction coin value 
    def __init__(self, sender, receiver, value):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'receiver': self.receiver,
            'value': self.value,
            'time': self.time
        })

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

#############################
transactions = []

P1 = Client()
P2 = Client()
P3 = Client()
P4 = Client()
P5 = Client()

t1 = Transaction(P1, P2.identity, 50.0)
t2 = Transaction(P2, P3.identity, 10.0)
t3 = Transaction(P3, P4.identity, 50.0)
t4 = Transaction(P4, P5.identity, 20.0)
t5 = Transaction(P5, P1.identity, 30.0)

t1.sign_transaction()
t2.sign_transaction()
t3.sign_transaction()
t4.sign_transaction()
t5.sign_transaction()

transactions.append(t1)
transactions.append(t2)
transactions.append(t3)
transactions.append(t4)
transactions.append(t5)

print(transactions)

