# ForexForecasterOptTrades

The aim of this project is to forecast exchange rates of several currencies using Facebook Prophet and then build a graph using predicted
exchange rates to find the optimal trades one should make in the future. The nodes of the graph are currencies at different dates and the
edges connecting them represent the gain/loss in value experienced by making a specific trade or holding on to a currency. Below you can
see a simplistic diagram of what the graph would look like.

<img width="526" alt="graph" src="https://user-images.githubusercontent.com/45244659/66863754-9de47b00-ef8b-11e9-9c32-b8e5e2f5de65.png">

Here A, B and C are three different currencies. Arrows between currencies on the same day represent trading between those currencies on
that day. Arrows between the same currency from Day 0 to Day 1 represents holding on to that currency from Day 0 to Day 1.

## How to use the code

The first thing you will need to do is make a free account on currencylayer.com which gives you 250 free API requests. You will get an
access key which you should put in line 19 of currencydata.py. You can then run currencydata.py and currencymodel.py. You will need to
replace the date in line 43 of graphalgos.py with the date in the first rows of currency_model.csv and test_set.csv. Use this same date 
in place of the date on line 20 of currencypath.py. Use the date in the last rows of the csv files in line 21 of currencypath.py and 
then run currencypath.py.

Since currencylayer's free version only gives 250 API requests, I have written the code so that API requests are not made for daily 
data, but in intervals of 3 days to capture some yearly seasonality. The base currency used to measure the values of all other 
currencies is USD. We use the first 200 datapoints (equally spaced across 600 days) to predict the next 50 values (equally spread across 
150 days). currencypath.py produces the optimal path to take, based on predictions from Facebook Prophet. If the path has [...2019-10-15 
USDEUR, 2019-10-18  USDEUR...] it means we should hold on to EUR from 15th Oct to 18th Oct. If the path has [...2019-10-15  USDEUR, 
2019-10-15  USDJPY...] it means on 15th Oct we should trade EUR for JPY. currencypath.py also uses the last 50 datapoints from the real 
data to evaluate the predictions made by the model.

In its current state, the Prophet model is very simplistic and does a poor job of modelling the trend in the currencies. As a result, 
the predicted path would give hardly any profit and is nowhere near the optimal path. A better Prophet model or a different machine 
learning algorithm may give a more accurate model which should give more profitable paths using the same graph algorithms.

## Future improvements

The main area that needs to be improved in this project is the model produced in currencymodel.py. I plan to play around with different
parameters of Facebook Prophet such as multiplicative seasonalities, different Fourier orders for seasonalities and impact of country
specific holidays. Hopefully a better model will be produced which will give more reliable results.

I plan to improve the coding style so that users do not have to manually change dates throughout the scripts but the program should
automatically find the required dates in the csv files and use them. Ideally, a user should only have to enter their access key in
currencydata.py and then run all 3 scripts.

I intend to add functionality for a variable interval between datapoints instead of a predetermined value (3) set by me. This would mean
users have to add an extra input but have greater control over their data. I may also add functionality for a variable number of API
requests for users who may have purchased higher end currencylayer packages.

Similarly, I plan to add functionality for different splits of the dataset into training and test sets. This may be especially useful
if the model is improved to give reliable results and a user wants to spend all 250 of their requests to predict the future trades to
make without further testing. I may also add functionality for changing the currencies that are being used in the project.
