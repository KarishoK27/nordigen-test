from nordigen.celery import app
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.conf import settings
import requests

from .models import AccessToken, UserAgreement, UserAccount

logger = get_task_logger(__name__)

@app.task(name="get_account_data")
def get_account_data(user_agreement):
    token = get_access_token()
    accounts = UserAccount.objects.filter(user_agreement__id=user_agreement)
    data = []
    for account in accounts:
        data = {
            'account': account,
            'transactions': get_account_transactions(token, account) 
        }
    return data

def get_access_token():
    token = AccessToken.objects.first()
    if token:
        if token.access_expires.replace(tzinfo=None) <= datetime.now().replace(
                tzinfo=None):
            if token.refresh_expires.replace(
                    tzinfo=None) <= datetime.now().replace(tzinfo=None):
                token = get_new_access_token(token)
            else:
                token = refresh_access_token(token)
    else:
        token = AccessToken()
        token = get_new_access_token(token)

    return token.access_token


def get_new_access_token(token):
    response = requests.post(f'{settings.API_BASE_URL}/api/v2/token/new/',
                             data={
                                 'secret_id': settings.API_SECRET_ID,
                                 'secret_key': settings.API_SECRET_KEY
                             })
    token_data = response.json()
    token.access_token = token_data['access']
    token.access_expires = datetime.now() + timedelta(
        seconds=token_data['access_expires'])
    token.refresh_token = token_data['access']
    token.refresh_expires = datetime.now() + timedelta(
        seconds=token_data['refresh_expires'])
    token.save()
    return token


def refresh_access_token(token):
    response = requests.post(f'{settings.API_BASE_URL}/api/v2/token/refresh/',
                             data={'refresh': token.refresh_token})
    token_data = response.json()
    token.access_token = token_data['access']
    token.access_expires = datetime.now() + timedelta(
        seconds=token_data['access_expires'])
    token.save()
    return token


def get_institutions(token, country='LV'):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {'country': country}
    response = requests.get(f'{settings.API_BASE_URL}/api/v2/institutions/',
                            params=payload,
                            headers=headers)
    return response.json()


def create_user_agreement(token, institution_id = 'SANDBOXFINANCE_SFIN0000'):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {'institution_id': institution_id}
    response = requests.post(f'{settings.API_BASE_URL}/api/v2/agreements/enduser/',
                            data=data,
                            headers=headers)
    data = response.json()
    user_agreement = UserAgreement()
    user_agreement.institution_id = data['institution_id']
    user_agreement.agreement = data['id']
    user_agreement.created_at = data['created']
    user_agreement.save()
    
    return user_agreement


def build_link(token, user_agreement):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        'redirect': f'{settings.HOST_ADDRESS}/account', 
        'institution_id': user_agreement.institution_id,
        'reference': user_agreement.id, 
        'agreement': user_agreement.agreement, 
    }
    response = requests.post(f'{settings.API_BASE_URL}/api/v2/requisitions/',
                            data=data,
                            headers=headers)
    data = response.json()

    user_agreement.requisition_id = data['id']
    user_agreement.link = data['link']
    user_agreement.save()

    return user_agreement


def get_accounts(token, user_agreement):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{settings.API_BASE_URL}/api/v2/requisitions/{user_agreement.requisition_id}/',
                            headers=headers)
    data = response.json()
    
    accounts = []
    for a in data['accounts']:
        UserAccount.objects.get_or_create(
            agreement=user_agreement,
            account=a)
        accounts.append({'account': a})
    return accounts


def get_account_transactions(token, account):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{settings.API_BASE_URL}/api/v2/accounts/{account}/transactions/',
                            headers=headers)
    return response.json()
    
            