import os
import random
import string
import qrcode
import bcrypt
import pymysql
from datetime import date
import json

def handle(event, context):
    conn = pymysql.connect(
        host="mariadb.default.svc.cluster.local",
        user="root",
        password="my_secret_pwd",
        database="cofrapdb"
    )
    data = json.loads(event.body)
    username = data.get("username")
    try:
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "images/qrcode.png")

        salt = b"$2b$12$wJ6vQwQwQwQwQwQwQwQwQ."
        pwd = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation, k=25))
        hashPWD = bcrypt.hashpw(pwd.encode(), salt)
        qrcodeImg = qrcode.make(pwd)
        qrcodeImg.save(output_path)

        gendate = date.today().strftime("%Y-%m-%d")
        # StoreInBDD
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, password, gendate) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, hashPWD.decode(), gendate))
            conn.commit()

        return {
                "statusCode": 200,
                "body": f"done -> {pwd}"
            }
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Affiche la stacktrace dans les logs du pod
        return {
            "statusCode": 500,
            "body": f"Erreur durant le traitement : {str(e)}"
        }
