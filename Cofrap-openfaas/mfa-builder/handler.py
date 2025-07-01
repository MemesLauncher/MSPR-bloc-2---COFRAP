import os
import random
import string
import qrcode
import bcrypt
import pymysql
import json

def handle(event, context):
    try:
        data = json.loads(event.body)
        username = data.get("username")  # On suppose que le username est passé dans le body
        salt = b"$2b$12$wJ6vQwQwQwQwQwQwQwQwQ."
        caracteres = string.ascii_letters + string.digits + string.punctuation
        caracteres = caracteres.replace('\\', '')
        MFA = ''.join(random.choices(caracteres, k=25))
        hashMFA = bcrypt.hashpw(MFA.encode(), salt)

        # Génération du QR code (optionnel)
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "images/qrcode.png")
        qrcodeImg = qrcode.make(MFA)
        qrcodeImg.save(output_path)

        # Connexion à la base
        conn = pymysql.connect(
            host="mariadb.default.svc.cluster.local",
            user="root",
            password="my_secret_pwd",
            database="cofrapdb"
        )
        with conn.cursor() as cursor:
            # Vérifier si l'utilisateur existe
            cursor.execute("SELECT 1 FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if not result:
                return {
                    "statusCode": 404,
                    "body": f"Utilisateur {username} non trouvé"
                }
            # Mettre à jour le MFA
            sql = "UPDATE users SET MFA=%s WHERE username=%s"
            cursor.execute(sql, (hashMFA.decode(), username))
            conn.commit()

        return {
            "statusCode": 200,
            "body": f"MFA généré et stocké pour {username} -> {MFA}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erreur durant le traitement : {str(e)}"
        }