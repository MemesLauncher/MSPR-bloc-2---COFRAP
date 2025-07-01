from django.urls import path
from .views import create_account, create_account_form, login_form, account_page, login_api

urlpatterns = [
    path('create/', create_account, name='create_account'),
    path('form/', create_account_form, name='create_account_form'),
    path('login/', login_form, name='login_form'),
    path('account/', account_page, name='account_page'),
    path('login-api/', login_api, name='login_api'),  # <-- Ajouté ici
]