import os
import bcrypt

def handle(event, context):
    try:
        username = event.body
        password = event.body
        salt = b"$2b$12$wJ6vQwQwQwQwQwQwQwQwQ."
        getpwd = "a".encode()
        password_to_verify = event.body
        if bcrypt.checkpw(password_to_verify, getpwd):
            return {
                    "statusCode": 200,
                    "body": f"Yup"
                }
        else:
            return {
                    "statusCode": 202,
                    "body": f"Nope"
                }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erreur durant le traitement : {str(e)}"
        }