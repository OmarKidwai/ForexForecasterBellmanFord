# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:32:23 2019

@author: omark
"""

"""[1] Gets historical data for exchange rates.

Gets prices of 4 predetermined currencies in USD from currencylayer. Since the
free version of currencylayer gives only 250 API requests, the data is taken
in intervals of 3 days instead of being daily data. 
"""

import requests
import pandas as pd
import datetime as dt

ACCESS_KEY = ""
rows = []
enddate = dt.date.today() - dt.timedelta(days=1)

for x in range(250):
    # Each iteration gets data for one date.
    date = enddate - dt.timedelta(days=x * 3)
    # date iterates over intervals of 3 days.
    parameters = {
        "access_key": ACCESS_KEY,
        "date": date.isoformat(),
        "currencies": "EUR,JPY,GBP,AUD",
    }
    # A new access key will be required to repeat this.
    request = requests.get("http://apilayer.net/api/historical", parameters)
    if request.status_code == 104:
        # 104 is the status code for API limit exceeded.
        # This condition was placed to be safe from an error on currencylayer's
        # side if they stopped giving more requests before the designated 250
        # requests had been exhausted.
        break
    if request.status_code != 200:
        print("error for", date)
        # 200 is the status code for success.
        # This condition was placed in case any request in the middle threw an
        # error, to ensure previously collected data was safe and the program
        # would keep getting data for the remaining dates.
        continue
    try:
        print("accessed", date)
        quotes = request.json()["quotes"]
        # Gets the dictionary with the 4 exchange rates.
        quotes["ds"] = request.json()["date"]
        # Adds the datestamp to the dictionary
        rows.append(quotes)
    except KeyError:
        break

rows.reverse()
# The loop iterates backwards from the most recent date. It is reversed to make
# it in chronological order.
df = pd.DataFrame(rows)
# Makes a dataframe with 5 columns for datestamp and the four currencies.

df.to_csv("currency_data.csv")
