import requests, names

def error_parse(cc, month, year, cvv, response_json):
    if 'incorrect_cvc' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Incorrect CVV )')
    if 'invalid_account' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Invalid Account )')
    if 'incorrect_number' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Incorrect Number )')
    if 'do_not_honor' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Do Not Honor )')
    if 'lost_card' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Lost Card )')
    if 'stolen_card' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Stolen Card )')
    if 'transaction_not_allowed' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Transaction Not Allowed )')
    if 'pickup_card' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Pickup Card )')
    if 'Your card has expired' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Expired )')
    if 'processing_error' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Processing Error )')
    if 'service_not_allowed' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Service Not Allowed )')
    if 'insufficient_funds' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Insufficient Funds )')
    if 'fraudulent' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Approved ( Fraudulent )')
    if 'Your card number is incorrect' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Incorrect CC )')
    if 'invalid_expiry_month' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Invalid Expiry Month )')
    if 'invalid_expiry_year' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Invalid Expiry Year )')
    if 'invalid_cvc' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Invalid CVC )')
    if 'card_declined' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Card Declined )')
    # if 'cvc' in response_json['payment_method_details']['card']['checks']['cvc_check']:
    #     return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Fail )')
    if 'generic_decline' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined')
    if 'unchecked' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Declined ( Unchecked )')
    else:
        return print(response_json)

def success_parse(cc, month, year, cvv, response_json):
    if 'Payment Complete.' in response_json['outcome']['seller_message']:
        return print(f'{cc}|{month}|{year}|{cvv} - Approved')
    if 'incorrect_cvc' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Approved ( Incorrect CVV )')
    if 'pass' in response_json['payment_method_details']['card']['checks']['cvc_check']:
        return print(f'{cc}|{month}|{year}|{cvv} - Approved')
    if 'fraudulent' in str(response_json):
        return print(f'{cc}|{month}|{year}|{cvv} - Approved ( Fraudulent )')
    else:
        return print(response_json)

def check(sk, combos):
    cc, month, year, cvv = combos.split('|')
    name, last = names.get_full_name().split(' ')

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    #source request
    data_source = f'type=card&owner[name]=carolprogay&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={month}&card[exp_year]={year}'
    response_source = requests.post('https://api.stripe.com/v1/sources', headers=headers, data=data_source, auth=(sk, '')).json()
    try:
        token_source = response_source['id']
    except:
        error_parse(cc, month, year, cvv, response_source)
        return False

    #charge request
    data_customer = f'description={name} {last}&source={token_source}'
    response_customer = requests.post('https://api.stripe.com/v1/customers', headers=headers, data=data_customer, auth=(sk, '')).json()
    try:
        token_customer = response_customer['id']
    except:
        error_parse(cc, month, year, cvv, response_customer)
        return False

    data_charges = f'amount=50&currency=usd&customer={token_customer}'
    response_charges = requests.post('https://api.stripe.com/v1/charges', headers=headers, data=data_charges, auth=(sk, '')).json()
    try:
        token_charges = response_charges['id']
        success_parse(cc, month, year, cvv, response_charges)
    except:
        error_parse(cc, month, year, cvv, response_charges)
        return False
    
    try:
        data_refunds = f'charge={token_charges}'
        response_refunds = requests.post('https://api.stripe.com/v1/refunds', headers=headers, data=data_refunds, auth=(sk, '')).json()
    except:
        error_parse(cc, month, year, cvv, response_charges)
        return False

sk = '' #your secret key
combos = input('Combos [Example 5201509856995697|12|26|414]: ')
check(sk, combos)