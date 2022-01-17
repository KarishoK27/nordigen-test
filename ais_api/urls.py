from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.account, name='account'),

    #API
    path('api/get_institutions', views.api_get_institutions, name='api_get_institutions'),
    path('api/create_agreement', views.api_create_agreement, name='api_create_agreement'), 
    path('api/get_account_transactions', views.api_get_account_transactions, name='api_get_account_transactions'), 
]
