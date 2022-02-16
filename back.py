import flask
from flask import Flask
import pandas as pd
import numpy as np
from COT.UpdateCFTCCOT import get_by_country
from fundamentals import get_financial_report
from news import get_news
import pickle, base64
from flask import Flask, render_template,request
from flask import url_for, jsonify
from flask_cors import CORS
from econ_data import get_econ


app = Flask(__name__, static_url_path='/')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/econ_data', methods=['POST'])
def ecofin():
    try:
        content = request.get_json()
        #print(content)
        sym = content['symbol'].upper()
        print(sym)
        df = get_econ(sym)
        print(df)
        pickled = pickle.dumps(df)
        pickled_b64 = base64.b64encode(pickled)
    except Exception as err:
        print(f'Other error occurred: {err}')
    return (pickled_b64)

@app.route('/fin_reports', methods=['POST'])
def resfin():
    try:
        content = request.get_json()
        #print(content)
        sym = content['symbol'].upper()
        df = get_financial_report(sym)
        pickled = pickle.dumps(df)
        pickled_b64 = base64.b64encode(pickled)
    except Exception as err:
        print(f'Other error occurred: {err}')
    return (pickled_b64)

@app.route('/news', methods=['POST'])
def resnews():
    try:
        content = request.get_json()
        #print(content)
        df = get_news(content['symbol'], content['days'])
        del df['_id']
        pickled = pickle.dumps(df)
        pickled_b64 = base64.b64encode(pickled)
    except Exception as err:
        print(f'Other error occurred: {err}')
    return (pickled_b64)

@app.route('/cot', methods=['POST'])
def rescot():
    try:
        content = request.get_json()
        #print(content)
        df = get_by_country(content['symbol'], content['number'])
        #print(df)
        pickled = pickle.dumps(df)
        pickled_b64 = base64.b64encode(pickled)
    except Exception as err:
        print(f'Other error occurred: {err}')
    return (pickled_b64)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=5001)
