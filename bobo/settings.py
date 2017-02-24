import boto3
from base64 import b64decode
kms = boto3.client('kms')

FIREBASE = {
    'apiKey':  kms.decrypt(CiphertextBlob=b64decode('FIREBASE_APIKEY'))['Plaintext'],
    'authDomain': kms.decrypt(CiphertextBlob=b64decode('FIREBASE_AUTH_DOMAIN'))['Plaintext'],
    'databaseURL': kms.decrypt(CiphertextBlob=b64decode('FIREBASE_DATABASE_URL'))['Plaintext'],
    'storageBucket': kms.decrypt(CiphertextBlob=b64decode('FIREBASE_STORAGE_BUCKET'))['Plaintext'],
    'messagingSenderId': kms.decrypt(CiphertextBlob=b64decode('FIREBASE_MESSAGING_SENDER_ID'))['Plaintext'],
}
DEFAULT_TEAM = 'team'
