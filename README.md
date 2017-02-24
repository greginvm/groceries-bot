# Lambas

## Alexa

Prepare ZIP and upload it manually.

```
cd alexa
AWS_PROFILE=profile lambda-uploader . --extra-files ../bobo --extra-files ../google --no-upload
```
## Example lambda.json configuration

```
{
    "name": "alexa-bobo",
    "description": "BOBO lambda for Alexa",
    "region": "us-east-1",
    "handler": "lambda.lambda_handler",
    "role": "arn:aws:iam::581942046872:role/service-role/alexa-bobo",
    "requirements": ["requests==2.10.0", "Pyrebase==3.0.27", "protobuf"],
    "ignore": [
        "localsettings.py",
        "lambda.json",
        ".git",
        "/*.zip"
    ],
    "timeout": 30,
    "memory": 512,
    "vpc": {}
}
```
