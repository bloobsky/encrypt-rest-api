import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from api.conf import SECRET_KEY


def hash_password(password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        hashes.SHA256(),
        32,
        salt,
        100000,
        backend=default_backend())
    key = kdf.derive(password.encode())
    return base64.b64encode(key).decode(), base64.b64encode(salt).decode()


def check_password(password, stored_hash, stored_salt):
    salt = base64.b64decode(stored_salt.encode())
    kdf = PBKDF2HMAC(
        hashes.SHA256(),
        32,
        salt,
        100000,
        backend=default_backend())
    try:
        kdf.verify(password.encode(), base64.b64decode(stored_hash.encode()))
        return True
    except BaseException:
        return False


def encrypt(text):
    iv = os.urandom(12)
    cipher = Cipher(
        algorithms.AES(SECRET_KEY),
        modes.GCM(iv),
        backend=default_backend())
    enc = cipher.encryptor()
    ct = enc.update(text.encode()) + enc.finalize()
    return base64.b64encode(iv + enc.tag + ct).decode()


def decrypt(data):
    raw = base64.b64decode(data.encode())
    iv = raw[:12]
    tag = raw[12:28]
    ct = raw[28:]
    cipher = Cipher(
        algorithms.AES(SECRET_KEY),
        modes.GCM(
            iv,
            tag),
        backend=default_backend())
    dec = cipher.decryptor()
    return (dec.update(ct) + dec.finalize()).decode()
