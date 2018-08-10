# web API currency convertor for Kiwi.com
# Written by Martin Kubicek
# python version 3.7
# last version 10.8.2018

from flask import Flask, jsonify, request
import argparse
import json
import requests

inJSON = dict()
outJSON = dict()

# Own dictionary with all know symbols or codes for all aviable currency
currDict = {'AUD':"AUD", 'A$':"AUD", 'AU$':"AUD", 'BGN':"BGN", 'лв.':"BGN", 'BRL':"BRL", 'R$':"BRL", 'CAD':"CAD", 'C$':"CAD",'CA$':"CAD", 'Can$':"CAD", 'CHF':"CHF", 'Fr.':"CHF", 'CNY':"CNY", '¥':"CNY", '元':"CNY",
'CZK':"CZK", 'Kč':"CZK", 'DKK':"DKK", 'kr.':"DKK", 'EUR':"EUR", '€':"EUR", 'GBP':"GBP", '£':"GBP", 'HKD':"HKD", 'HK$':"HKD", 'HRK':"HRK", 'kn':"HRK", 'HUF':"HUF", 'Ft':"HUF", 'IDR':"IDR", 'Rp':"IDR", 'ILS':"ILS", '₪':"ILS", 'INR':"INR", '₹':"INR", 'ISK':"ISK", 'Íkr':"ISK", 'JPY':"JPY", 'JP¥':"JPY", '円':"JPY", 'KRW':"KRW", '₩':"KRW", 'MXN':"MXN", 'Mex$':"MXN", 'MYR':"MYR", 'RM':"MYR", 'NOK':"NOK", 'NZD':"NZD", 'NZ$':"NZD", 'PHP':"PHP", '₱':"PHP", 'PLN':"PLN", 'zł':"PLN", 'RON':"RON", 'RUB':"RUB", '₽':"RUB", 'руб':"RUB", 'р.':"RUB", 'SEK':"SEK", 'SGD':"SGD", 'S$':"SGD", 'THB':"THB", '฿':"THB", 'TRY':"TRY", 'TL':"TRY", '₺':"TRY", 'USD':"USD", '$':"USD", 'US$':"USD", 'ZAR':"ZAR", 'R':"ZAR", 'None':None, None:None}

#getRequest: Getting actual currency conversion from Central Europian Bank
def getRequest(url):

	req = requests.get(url)
	requestJSONdata = req.json()

	return requestJSONdata

#getRates: decoding rates from JSON and using for calculating new amount of currency
def getRates(inCurren, outCurren, amount):

	global inJSON
	global outJSON

	if outCurren:
		url = "https://ratesapi.io/api/latest?base="+inCurren+"&symbols="+outCurren
		currencyJSONData = getRequest(url)

		inJSON = {"amount":amount, "currency":inCurren}
		outJSON = {outCurren:(amount*currencyJSONData['rates'][outCurren])}
		
	else:
		url = "https://ratesapi.io/api/latest?base="+inCurren
		currencyJSONData = getRequest(url)
		ratesJSONData = currencyJSONData['rates']

		inJSON = {"amount":amount, "currency":inCurren}

		for curreRates in ratesJSONData:
			outJSON[curreRates] = (amount*ratesJSONData[curreRates])

app = Flask(__name__)

#currency_converter: define route for REST API using Flask
@app.route('/currency_converter', methods=['GET', 'POST'])
def currency_converter():
	
	outCurren = None

	amount = request.args.get('amount', type = float)
	inCurren = request.args.get('input_currency')
	outCurren = request.args.get('output_currency')


	if (inCurren in currDict) and (outCurren in currDict):
		getRates(currDict[inCurren], currDict[outCurren], amount)
	else:
		return "Error:Currency not found"

	return jsonify(input=inJSON, output=outJSON)