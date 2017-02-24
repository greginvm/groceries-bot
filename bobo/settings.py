from base64 import b64decode
import boto3

def decrypt(key):
    try:
        kms = boto3.client('kms')
        return kms.decrypt(CiphertextBlob=b64decode(key))['Plaintext'],
    except:
        return ''

FIREBASE = {
    'apiKey':  decrypt('FIREBASE_APIKEY'),
    'authDomain': decrypt('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': decrypt('FIREBASE_DATABASE_URL'),
    'storageBucket': decrypt('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': decrypt('FIREBASE_MESSAGING_SENDER_ID'),
}
DEFAULT_TEAM = 'team'
DEFAULT_LIST = 'groceries'

try:
    from localsettings import *
except:
    print 'Failed to load local settings'
