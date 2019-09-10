import requests


def get_oil_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'Olje':
            return i['value']


def get_gold_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'Gull':
            return i['value']


def get_chf_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'CHF':
            return i['value']


def get_eur_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'EUR':
            return i['value']


def get_gbp_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'GBP':
            return i['value']


def get_sek_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'SEK':
            return i['value']


def get_usd_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'USD':
            return i['value']


def get_oseax_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'OSEAX':
            return i['value']


def get_osebx_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'OSEBX':
            return i['value']


def get_oslenx_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'OSLENX':
            return i['value']


def get_oslsfx_current_price():
    response = requests.get('https://finansavisen.no/json/stock')
    for i in response.json():
        if i['name'] == 'OSLSFX':
            return i['value']


def get_indeces():
    response = requests.get('https://finansavisen.no/json/stock').json()
    return {i['name']: i['value'] for i in response}