# MSPR-bloc-2---COFRAP
MSPR Bloc 2 - EPSI I2

# Lien rapport final
[Rapport MSPR2.docx](https://ifagparis-my.sharepoint.com/:w:/g/personal/anthony_tran1_ecoles-epsi_net/EQpg8Wca9QNNtMIDltgV4d0BrdLtTCOj4ZMgbvR8YYfUaA?e=zNX7XP)

# Guideline du projet
Durée maximum d'un sprint : 3 semaines<br>
Fréquence des réunions : Weekly (lundi soir)


# Technologies
Kubernetes<br>
K8s<br>
Minikube<br>
Maria DB<br>
Python

# Livrable
[CDC Technique](https://ifagparis-my.sharepoint.com/:w:/r/personal/francois_goudet_ecoles-epsi_net/Documents/CDC%20Technique.docx?d=wf34460c7be8a4b70b5b413340151f6ab&csf=1&web=1&e=qpSWQt)<br>
[CDC Fonctionnel](https://ifagparis-my.sharepoint.com/:w:/r/personal/francois_goudet_ecoles-epsi_net/Documents/CDC%20Fonctionnel.docx?d=we201757056f44991aa19af07af99bc63&csf=1&web=1&e=6TcU2f)

# Commandes d'initialisation du projet openfaas

<b>Installation d'openFaaS : </b>  <br>
`helm repo add openfaas https://openfaas.github.io/faas-netes/`  <br>
`helm repo update`  <br>

<b>Création des namespaces : </b>  <br>
`kubectl create namespace cofrap`  <br>
`kubectl create namespace cofrap-fn`<br>

<b>Déploiement d'openfaas dans les namespaces et liaison du namespace fonction :</b> <br>
`helm upgrade openfaas openfaas/openfaas --install --namespace cofrap --set functionNamespace=cofrap-fn --set basic_auth=true` <br>

<b>Récupération du mot de passe admin du namespace (A noter): </b><br>
`[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($(kubectl -n cofrap get secret basic-auth -o jsonpath="{.data.basic-auth-password}")))`        <b>/!\ A EXECUTER SUR POWERSHELL ADMIN /!\ </b><br>

<b>Hosting et accès à l'interface OpenFaaS : </b> <br>
`kubectl port-forward -n cofrap svc/gateway 8080:8080`  <br>
`localhost:8080`  <br>

![image](https://github.com/user-attachments/assets/2139bc47-c47c-4fba-a3e0-eef12ffa2a1c)

# Gestion de la DB

## Creation du kube mariaDB
1- Se déplacer dans le dossier 'cofrap-openfaas' <br>
2- faire la commande `kubectl apply -f mariadb-deployement.yaml`<br>

## Connexion a mariaDB

`kubectl get pods -n default` <br>
`kubectl exec -it <nom-du-pod> -- mariadb -u root -p`

<b>mdp = my_secret_pwd</b>

## Creation de la DB

-- Création de la base de données <br>
`CREATE DATABASE IF NOT EXISTS cofrapdb;` <br>
`USE cofrap;`<br>

-- Création de la table user <br>
`CREATE TABLE users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NULL,
    password VARCHAR(255) NULL,
    MFA VARCHAR(255) NULL,
    gendate DATETIME NULL,
    expired TINYINT DEFAULT 0 NULL
);`

# Mise en place des fonctions

1- Se déplacer dans le dossier 'cofrap-openfaas' <br>
2- faire la commande `faas-cli up -f stack.yaml`<br>

# Gestion du front

`pip install -r requirements.txt` <br>
`cd cofrap_web`<br>
`py manage.py runserver`<br>
