from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from .models import UserAgreement
from .tasks import get_account_data, get_access_token, get_accounts, get_institutions, create_user_agreement, build_link, get_account_transactions


def index(request):
    countries = [
        "NO", "SE", "FI", "DK", "EE", "LV", "LT", "GB", "NL", "CZ", "ES", "PL",
        "BE", "DE", "AT", "BG", "HR", "CY", "FR", "GR", "HU", "IS", "IE", "IT",
        "LI", "LU", "MT", "PT", "RO", "SK", "SI"
    ]
    return render(request, 'ais/index.html', {'countries': countries})

def account(request):
    ref = request.GET.get('ref', None)
    try:
        user_agreement = UserAgreement.objects.get(id=ref)
        token = get_access_token()
        accounts = get_accounts(token, user_agreement)
        get_account_data.delay(user_agreement.id)     
        data = {
            'accounts': accounts
        }
    except UserAgreement.DoesNotExist:
        data = {}
    return render(request, 'ais/account.html', data)


def api_get_institutions(request):
    county = request.GET.get('country', 'LV')
    token = get_access_token()
    data = get_institutions(token, county)
    return JsonResponse(data, safe=False)

def api_create_agreement(request):
    institution_id = request.POST.get('institution_id', None)
    token = get_access_token()
    user_agreement = create_user_agreement(token, institution_id)
    user_agreement = build_link(token, user_agreement)
    return JsonResponse({'url': user_agreement.link}, safe=False)

def api_get_account_transactions(request):
    account = request.GET.get('account', None)
    token = get_access_token()
    transactions = get_account_transactions(token, account)
    return JsonResponse(transactions, safe=False)