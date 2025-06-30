import os
import random
import string
import qrcode

def handle(event, context):
    try:
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "images/qrcode.png")

        pwd = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation, k=25))
        qrcodeImg = qrcode.make(pwd)
        qrcodeImg.save(output_path)
        # StoreInBDD
        return {
                "statusCode": 200,
                "body": f"{context.body()}"
            }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erreur durant le traitement : {str(e)} direction : {os.listdir(base_dir)}"
        }
