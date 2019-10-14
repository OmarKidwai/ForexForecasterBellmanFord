# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:28:57 2019

@author: omark
"""

"""[2] Takes historical data for exchange rates and predicts future values.

Takes the dataframe produced in currencydata.py and splits it into a training
set of 200 dates and a test set. Uses the training set to make a model using
Facebook Prophet for each of the 4 currencies for the dates in the test set.
Saves the test set and the predicted values for those dates.
"""

import pandas as pd
from fbprophet import Prophet

df = pd.read_csv("currency_data.csv")

train_set = df[:200]
test_set = df[199:]
# Starts from the 200th row and not the 201st since the algorithm in the next
# file will predict which trades to make starting with the current rates (200th)
# and based on predictions for the next 50 dates (201st - 249th)
dframe = test_set["ds"]
# A column of all the dates to be predicted.
test_set.to_csv("test_set.csv")
# Saves the test set for future use.

currencies = ["USDEUR", "USDJPY", "USDGBP", "USDAUD"]
for c in currencies:
    # Each iteration makes the model and predictions for one currency.
    data = train_set.loc[:, [c, "ds"]]
    # Selects the dates and rates only for one currency.
    data.rename(columns={c: "y"}, inplace=True)
    # Making the dataframe into the format expected by Facebook Prophet.
    model = Prophet(yearly_seasonality=True)
    model.fit(data)
    # Very basic Prophet model with minimal hyperparameter tuning.

    future = model.make_future_dataframe(periods=150)
    # 150 because dates are in intervals of 3 days and make_future_dataframe
    # gives consecutive dates.
    history = future[:200]
    # history has dates which were fed to the model which are in the intervals.
    future = future[200:]
    bool_mask = []
    for x in range(50):
        bool_mask.append(False)
        bool_mask.append(False)
        bool_mask.append(True)
    future = future.iloc[bool_mask]
    # Makes future into intervals of 3 days.
    future = pd.concat([history, future], ignore_index=True)

    forecast = model.predict(future)
    # Produces the forecast for the required dates.
    fig = model.plot(forecast)
    # Helps with visualisation.
    forecast = forecast[199:]
    col = forecast["yhat"]
    # A column of the predicted values.
    dframe = pd.concat([dframe, col], axis=1)
    # Concatenates col with the dates and values already predicted for other
    # currencies.
    dframe.rename(columns={"yhat": c}, inplace=True)
    # Renamed back to the name of the currency pairs.
    # dframe now has the same columns that test_set had.

dframe.to_csv("currency_model.csv")
