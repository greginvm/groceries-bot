'''
Follow these steps to configure the slash command in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new
  2. Search for and select "Slash Commands".
  3. Enter a name for your command and click "Add Slash Command Integration".
  4. Copy the token string from the integration settings and use it in the next section.
  5. After you complete this blueprint, enter the provided API endpoint URL in the URL field.


To encrypt your secrets use the following steps:
  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html
  2. Click the "Enable Encryption Helpers" checkbox
  3. Paste <COMMAND_TOKEN> into the kmsEncryptedToken environment variable and click encrypt

'''

import boto3
import json
import logging
import os

from base64 import b64decode
from urlparse import parse_qs

import handler
from bobo import settings


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != settings.SLACK['expected_token']:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    user = params['user_name'][0]
    command_text = params['text'][0]

    return respond(None, handler.trigger(user, command_text))
