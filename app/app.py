from flask import abort, Flask, request
import requests
from bs4 import BeautifulSoup
import redis


app = Flask(__name__)
db = redis.Redis("localhost")


def retrieve_rate(currency, reference_date):
    if not currency or not reference_date:
        return None

    key = reference_date + "|" + currency

    # Try to get the value from the db
    try:
        rate = float(db.get(key))
        return rate
    except (ValueError, TypeError):
        rate = None

    # If not in db, try and get value parsing the xml
    # Populate the db if the value is found in the xml
    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    response = requests.get(url)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, features='html.parser')
        elem = soup.select_one('cube>cube[time="{}"]>cube[currency="{}"]'.format(reference_date, currency))
        try:
            rate = float(elem['rate'])
            db.set(key, rate)
        except:
            rate = None
        finally:
            return rate

        


@app.route('/convert', methods=['GET'])
def convert():
    amount = request.args.get('amount', None)
    src_currency = request.args.get('src_currency', None)
    dest_currency = request.args.get('dest_currency', None)
    reference_date = request.args.get('reference_date', None)

    # Check params are correctly defined
    if not amount or not src_currency or not dest_currency \
       or not reference_date:
        abort(400)

    # Check conversion is only between eur and something else
    lower_src = src_currency.lower()
    lower_dest = dest_currency.lower()
    if (lower_src != 'eur' and lower_dest != 'eur') or \
       (lower_src == 'eur' and lower_dest == 'eur'):
        abort(400)


    if lower_src == 'eur':
        currency = dest_currency
    else:
        currency = src_currency

    rate = retrieve_rate(currency, reference_date)

    # Could not find the rate based on the parameters
    if not rate:
        abort(404)

    real_rate = 2-rate if lower_dest == 'eur' else rate

    return {'amount': float(amount)*real_rate,
            'currency': dest_currency}

