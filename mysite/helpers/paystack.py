import json

import requests
from requests.structures import CaseInsensitiveDict

from myapi.models import Payment, AuthCard


def create_vba(key, customer_id):
    headers = {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
    }

    data = {"customer": customer_id, "preferred_bank": "wema-bank"}

    response = requests.post('https://api.paystack.co/dedicated_account',
                             headers=headers, json=data)
    # print(response.text.encode('utf8'))

    return json.loads(response.text)


def verify_bvn(key, customer_code, bvn_number, first_name, last_name):
    headers = {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
    }

    data = {"country": "NG", "type": "bvn", "value": bvn_number,
            "first_name": first_name, "last_name": last_name}

    response = requests.post(
        f'https://api.paystack.co/customer/{customer_code}/identification',
        headers=headers, json=data)

    return response

def resolve_account(key, account_number, bank_code):
    

    url = f"https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {key}"

    # headers = {
    #     'Authorization': 'Bearer ' + key,
    #     'Content-Type': 'application/json',
    # }


    resp = requests.get(url, headers=headers)

    return json.loads(resp.text)

def charge_pay(key, auth_code, email, amount):

    headers = {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
    }

    data = { "amount": amount,
            "authorization_code": auth_code, "email": email}

    response = requests.post(
        f'https://api.paystack.co/transaction/charge_authorization',
        headers=headers, json=data)
    print(response.text)

    return response


def transaction_success(data):
    payment = Payment.objects.get(reference=data['reference'])
    payment.status = data['success']
    payment.amount = data['amount'] / 100
    payment.payment_date = data['paid_at']
    payment.description = data['message']
    payment.payment_mode = 'card'
    payment.save()
    authorization = AuthCard.objects.get_or_create(
        authorization_code='AUTH_f5rnfq9p', bin='539999', last4='8877',
        exp_month='08', exp_year='2020',
        card_type='mastercard DEBIT', bank='Guaranty Trust Bank',
        country_code='NG', brand='mastercard',
        account_name='BoJack Horseman', client=payment.client)
    authorization.save()
    return {'type': 'successful transaction'}


def transfer_failed(data):
    return {'type': 'failed transfer'}


def transfer_success(data):
    return {'type': 'successful transfer'}


def transfer_reversed(data):
    return {'type': 'reversed transfer'}


def customer_identification_success(data):
    pass


def customer_identification_failed(data):
    pass
