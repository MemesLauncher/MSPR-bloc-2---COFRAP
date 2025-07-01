import json
from datetime import datetime, timedelta
import pymysql
import bcrypt

def handle(event, context):
    data = json.loads(event.body)
    username = data.get("username")
    password = data.get("password")
    mfa = data.get("mfa")

    # Connexion à la base MariaDB avec pymysql
    conn = pymysql.connect(
        host="mariadb.default.svc.cluster.local",
        user="root",
        password="my_secret_pwd",
        database="cofrapdb",
        cursorclass=pymysql.cursors.Cursor
    )
    cursor = conn.cursor()

    # Récupère l'utilisateur
    cursor.execute("SELECT password, MFA, gendate, expired FROM users WHERE username=%s", (username,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return json.dumps({"error": "Utilisateur inconnu"}), 401

    db_password, db_mfa, gendate, expired = row

    # Vérifie le mot de passe et le MFA (hashés avec bcrypt)
    salt = b"$2b$12$wJ6vQwQwQwQwQwQwQwQwQ."
    try:
        password_ok = bcrypt.checkpw(password.encode(), db_password.encode())
        mfa_ok = bcrypt.checkpw(mfa.encode(), db_mfa.encode())
    except Exception:
        password_ok = False
        mfa_ok = False

    if not password_ok or not mfa_ok:
        cursor.close()
        conn.close()
        return json.dumps({"error": "Identifiants invalides"}), 401

    # Vérifie la date de génération du mot de passe
    if gendate:
        try:
            last_change = datetime.strptime(str(gendate), "%Y-%m-%d")
        except Exception:
            last_change = datetime.now()  # Si erreur de parsing, on ne bloque pas
        if last_change < datetime.now() - timedelta(days=180):
            # Expire le compte
            cursor.execute("UPDATE users SET expired=1 WHERE username=%s", (username,))
            conn.commit()
            cursor.close()
            conn.close()
            return json.dumps({
                "expired": True,
                "redirect": "/accounts/form/",
                "message": "Mot de passe expiré, veuillez le renouveler."
            }), 403

    # Si tout est OK
    cursor.close()
    conn.close()
    return json.dumps({"success": True, "message": "Connexion réussie"}), 200