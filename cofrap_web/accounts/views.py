import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

@csrf_exempt
def create_account(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            # Appel à la fonction OpenFaaS password-builder
            faas_url_pwd = "http://127.0.0.1:8080/function/password-builder"
            faas_response_pwd = requests.post(faas_url_pwd, json={"username": username})
            try:
                pwd_data = faas_response_pwd.json()
            except Exception:
                pwd_data = {"raw": faas_response_pwd.text}

            # Appel à la fonction OpenFaaS mfa-builder
            faas_url_mfa = "http://127.0.0.1:8080/function/mfa-builder"
            faas_response_mfa = requests.post(faas_url_mfa, json={"username": username})
            try:
                mfa_data = faas_response_mfa.json()
            except Exception:
                mfa_data = {"raw": faas_response_mfa.text}

            # Fusionne les résultats pour le front
            result = {
                "message": pwd_data.get("message", ""),
                "qrcode": pwd_data.get("qrcode", ""),
                "mfa_message": mfa_data.get("message", ""),
                "mfa_qrcode": mfa_data.get("qrcode", "")
            }
            return JsonResponse(result, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            mfa = data.get("mfa")
            # Appel à la fonction OpenFaaS login-handler
            faas_url = "http://127.0.0.1:8080/function/login-handler"
            faas_response = requests.post(faas_url, json={
                "username": username,
                "password": password,
                "mfa": mfa
            })
            try:
                result = faas_response.json()
            except Exception:
                result = {"body": faas_response.text}
            return JsonResponse(result, status=faas_response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)

def create_account_form(request):
    return render(request, 'create_account.html')

def login_form(request):
    return render(request, 'login.html')

def account_page(request):
    return render(request, 'account.html')