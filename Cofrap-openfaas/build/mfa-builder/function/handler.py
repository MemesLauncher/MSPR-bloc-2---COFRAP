import os
import random
import string
import qrcode
import bcrypt
import pymysql
import json
import base64
from io import BytesIO

def handle(event, context):
    try:
        data = json.loads(event.body)
        username = data.get("username")
        salt = b"$2b$12$wJ6vQwQwQwQwQwQwQwQwQ."
        caracteres = string.ascii_letters + string.digits + string.punctuation
        caracteres = caracteres.replace('\\', '')
        MFA = ''.join(random.choices(caracteres, k=25))
        hashMFA = bcrypt.hashpw(MFA.encode(), salt)

        # Génération du QR code
        qrcodeImg = qrcode.make(MFA)
        buffer = BytesIO()
        qrcodeImg.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()

        # Connexion à la base
        conn = pymysql.connect(
            host="mariadb.default.svc.cluster.local",
            user="root",
            password="my_secret_pwd",
            database="cofrapdb"
        )
        with conn.cursor() as cursor:
            # Vérifie si l'utilisateur existe et récupère expired et MFA
            cursor.execute("SELECT expired, MFA FROM users WHERE username=%s", (username,))
            row = cursor.fetchone()
            if not row:
                # Nouvel utilisateur : insert MFA et QR code
                cursor.execute(
                    "INSERT INTO users (username, MFA, expired) VALUES (%s, %s, 0)",
                    (username, hashMFA.decode())
                )
                conn.commit()
                return {
                    "statusCode": 201,
                    "body": json.dumps({
                        "message": "Utilisateur créé avec MFA",
                        "qrcode": qr_b64
                    })
                }
            expired, db_mfa = row
            # Si MFA est NULL ou vide, on en crée un
            if not db_mfa:
                cursor.execute(
                    "UPDATE users SET MFA=%s WHERE username=%s",
                    (hashMFA.decode(), username)
                )
                conn.commit()
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "MFA créé pour utilisateur existant",
                        "qrcode": qr_b64
                    })
                }
            if expired == 0:
                return {
                    "statusCode": 409,
                    "body": json.dumps({"error": "Utilisateur déjà existant"})
                }
            else:
                # Utilisateur existant et expiré, on régénère le MFA
                sql = "UPDATE users SET MFA=%s WHERE username=%s"
                cursor.execute(sql, (hashMFA.decode(), username))
                conn.commit()
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "MFA régénéré",
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