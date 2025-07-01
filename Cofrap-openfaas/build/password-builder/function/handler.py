import os
import random
import string
import qrcode
import bcrypt
import pymysql
from datetime import date
import json
import base64
from io import BytesIO

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
        caracteres = string.ascii_letters + string.digits + string.punctuation
        caracteres = caracteres.replace('\\', '')
        pwd = ''.join(random.choices(caracteres, k=25))
        hashPWD = bcrypt.hashpw(pwd.encode(), salt)
        qrcodeImg = qrcode.make(pwd)
        buffer = BytesIO()
        qrcodeImg.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()

        gendate = date.today().strftime("%Y-%m-%d")

        with conn.cursor() as cursor:
            # Vérifie si l'utilisateur existe déjà
            cursor.execute("SELECT expired FROM users WHERE username=%s", (username,))
            row = cursor.fetchone()
            if row:
                expired = row[0]
                if expired == 0:
                    return {
                        "statusCode": 409,
                        "body": json.dumps({"error": "Utilisateur déjà existant"})
                    }
                else:
                    # Utilisateur existant et expiré, on régénère un mot de passe
                    cursor.execute(
                        "UPDATE users SET password=%s, gendate=%s, expired=0 WHERE username=%s",
                        (hashPWD.decode(), gendate, username)
                    )
                    conn.commit()
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message": "Mot de passe régénéré",
                            "qrcode": qr_b64
                        })
                    }
            else:
                # Nouvel utilisateur
                cursor.execute(
                    "INSERT INTO users (username, password, gendate, expired) VALUES (%s, %s, %s, 0)",
                    (username, hashPWD.decode(), gendate)
                )
                conn.commit()
                return {
                    "statusCode": 201,
                    "body": json.dumps({
                        "message": "Utilisateur créé",
                        "qrcode": qr_b64
                    })
                }

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": f"Erreur durant le traitement : {str(e)}"
        }