# MSPR-bloc-2---COFRAP
MSPR Bloc 2 - EPSI I2

# Lien rapport final
https://ifagparis-my.sharepoint.com/:w:/r/personal/francois_goudet_ecoles-epsi_net/Documents/CDC%20Technique.docx?d=wf34460c7be8a4b70b5b413340151f6ab&csf=1&web=1&e=qpSWQt

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
CDC Technique : https://ifagparis-my.sharepoint.com/:w:/r/personal/francois_goudet_ecoles-epsi_net/Documents/CDC%20Technique.docx?d=wf34460c7be8a4b70b5b413340151f6ab&csf=1&web=1&e=qpSWQt<br>
CDC Fonctionnel : https://ifagparis-my.sharepoint.com/:w:/r/personal/francois_goudet_ecoles-epsi_net/Documents/CDC%20Fonctionnel.docx?d=we201757056f44991aa19af07af99bc63&csf=1&web=1&e=6TcU2f


# Commandes d'installation OpenFaaS (minikube)

helm repo add openfaas https://openfaas.github.io/faas-netes/ <br>
helm repo update

# Commandes d'initialisation du projet openfaas

kubectl create namespace cofrap  <br>
kubectl create namespace cofrap-fn<br>

<b>Déploiement d'openfaas dans les namespaces et liaison du namespace fonction :</b> <br>
helm upgrade openfaas openfaas/openfaas --install --namespace cofrap --set functionNamespace=cofrap-fn --set basic_auth=true <br>

<b>Récupération du mot de passe admin du namespace (A noter): </b><br>
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}"))) /!\ A FAIRE SUR POWERSHELL ADMIN /!\ <br>

<b>Hosting et accès à l'interface OpenFaaS : </b> <br>
kubectl port-forward -n cofrap svc/gateway 8080:8080  <br>
localhost:8080  <br>

