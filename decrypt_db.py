import pymongo
from api.conf import MONGODB_DBNAME
from api.crypto_utils import decrypt

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client[MONGODB_DBNAME]

for user in db.users.find({}):
    print('---')
    print('Email:', user.get('email'))
    print('Display Name:', decrypt(user.get('displayName', '')))
    print('Address:', decrypt(user.get('address', '')))
    print('Phone:', decrypt(user.get('phone', '')))
    print('DOB:', decrypt(user.get('dateOfBirth', '')))
    print('Disabilities:', decrypt(user.get('disabilities', '')))
    print('---')

