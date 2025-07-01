import json
import pymysql
import bcrypt

def handle(event, context):
    try:
        # Récupérer les données du body (JSON)
        data = json.loads(event.body)
        username = data.get("username")
        password = data.get("password")
        mfa_code = data.get("mfa")  # Nouveau champ pour le code MFA

        if not username or not password or not mfa_code:
            return {
                "statusCode": 400,
                "body": f"Username, password et code MFA requis {username}, {password}, {mfa_code}"
            }

        # Connexion à la base MariaDB
        conn = pymysql.connect(
            host="mariadb.default.svc.cluster.local",
            user="root",
            password="my_secret_pwd",
            database="cofrapdb"
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT password, MFA FROM users WHERE username=%s", (username,))
            row = cursor.fetchone()
            if row is None:
                return {
                    "statusCode": 401,
                    "body": "Utilisateur inconnu"
                }
            hashed_pwd = row[0].encode()
            hashed_mfa = row[1].encode() if row[1] else None

            if not bcrypt.checkpw(password.encode(), hashed_pwd):
                return {
                    "statusCode": 401,
                    "body": "Mot de passe incorrect"
                }
            if not hashed_mfa or not bcrypt.checkpw(mfa_code.encode(), hashed_mfa):
                return {
                    "statusCode": 401,
                    "body": "Code MFA incorrect"
                }
            return {
                "statusCode": 200,
                "body": "Connexion OK"
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erreur durant le traitement : {str(e)}"
        }
    finally:
        try:
            conn.close()
        except:
            pass