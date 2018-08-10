#!/usr/bin/env python3.7
# CLI currency convertor for Kiwi.com
# Written by Martin Kubicek
# python version 3.7
# last version 10.8.2018

import argparse
import json
import requests

# Own dictionary with all know symbols or codes for all aviable currency
currDict = {'AUD':"AUD", 'A$':"AUD", 'AU$':"AUD", 'BGN':"BGN", 'лв.':"BGN", 'BRL':"BRL", 'R$':"BRL", 'CAD':"CAD", 'C$':"CAD",'CA$':"CAD", 'Can$':"CAD", 'CHF':"CHF", 'Fr.':"CHF", 'CNY':"CNY", '¥':"CNY", '元':"CNY",
'CZK':"CZK", 'Kč':"CZK", 'DKK':"DKK", 'kr.':"DKK", 'EUR':"EUR", '€':"EUR", 'GBP':"GBP", '£':"GBP", 'HKD':"HKD", 'HK$':"HKD", 'HRK':"HRK", 'kn':"HRK", 'HUF':"HUF", 'Ft':"HUF", 'IDR':"IDR", 'Rp':"IDR", 'ILS':"ILS", '₪':"ILS", 'INR':"INR", '₹':"INR", 'ISK':"ISK", 'Íkr':"ISK", 'JPY':"JPY", 'JP¥':"JPY", '円':"JPY", 'KRW':"KRW", '₩':"KRW", 'MXN':"MXN", 'Mex$':"MXN", 'MYR':"MYR", 'RM':"MYR", 'NOK':"NOK", 'NZD':"NZD", 'NZ$':"NZD", 'PHP':"PHP", '₱':"PHP", 'PLN':"PLN", 'zł':"PLN", 'RON':"RON", 'RUB':"RUB", '₽':"RUB", 'руб':"RUB", 'р.':"RUB", 'SEK':"SEK", 'SGD':"SGD", 'S$':"SGD", 'THB':"THB", '฿':"THB", 'TRY':"TRY", 'TL':"TRY", '₺':"TRY", 'USD':"USD", '$':"USD", 'US$':"USD", 'ZAR':"ZAR", 'R':"ZAR", 'None':None}
#makeJSON: transforming string or dictionary to JSON output
def makeJSON(outJSON, inCurren):

	outJSONData = {}
	outJSONData["input"] = {"amount":amount, "currency":inCurren}
	outJSONData["output"] = outJSON
	outData = json.dumps(outJSONData, indent=2)
	
	print(outData)
	exit(0)

#getRequest: Getting actual currency conversion from Central Europian Bank
def getRequest(url):

	req = requests.get(url)
	requestJSONdata = req.json()

	return requestJSONdata

#getRates: decoding rates from JSON and using for calculating new amount of currency
def getRates(inCurren, outCurren):

	outJSON = dict()

	if outCurren:
		url = "https://ratesapi.io/api/latest?base="+inCurren+"&symbols="+outCurren
		currencyJSONData = getRequest(url)
		outJSON = {outCurren:(amount*currencyJSONData['rates'][outCurren])}

		makeJSON(outJSON, inCurren)
		
	else:
		url = "https://ratesapi.io/api/latest?base="+inCurren
		currencyJSONData = getRequest(url)
		ratesJSONData = currencyJSONData['rates']

		for curreRates in ratesJSONData:
			outJSON[curreRates] = (amount*ratesJSONData[curreRates])

		makeJSON(outJSON, inCurren)

#Starting part of code, parsing arguments and verifying
argParsers = argparse.ArgumentParser()
argParsers.add_argument("--amount", type = float, help = "amount which we want to convert",  required = True)
argParsers.add_argument("--input_currency", help = "input currency - 3 letters name or currency symbol",  required = True)
argParsers.add_argument("--output_currency", help = "requested/output currency - 3 letters name or currency symbol")
arguments = argParsers.parse_args()

inCurren = str(arguments.input_currency)
outCurren = str(arguments.output_currency)
amount = arguments.amount

#Transform symbols of currency to 3letter code
if (inCurren in currDict) and (outCurren in currDict):
	getRates(currDict[inCurren], currDict[outCurren])
else:
	print("Error:Currency not found")
	exit(0)
