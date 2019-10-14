# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 15:11:06 2019

@author: omark
"""

"""[3] Finds the optimal path based on predictions of currencies and evaluates
it.

Makes graphs from currency_model and test_set produced in currencymodel.py.
Finds the optimal path in currency_model, tests the path on the real data for
those dates and finds the actual optimal path in hindsight.
"""

from graphalgos import make_graph
from graphalgos import profit_in_specified_path
from graphalgos import optimal_path

s = "2019-05-09  "
t = "2019-10-06  "

model_graph = make_graph("currency_model.csv")
profit, path = optimal_path(model_graph, s, t)
print("Predicted Optimal Path: " + ", ".join(path))
# The path that the model predicts as most profitable which should be followed.
print("Predicted Profit: " + str(profit) + "%")
# The profit predicted on said path.
test_graph = make_graph("test_set.csv")
a_profit = profit_in_specified_path(test_graph, path)
print("Actual Profit with Predicted Path: " + str(a_profit) + "%")
# The actual profit that would be made if the path was followed in real time and
# the specified trades were made.
accuracy = a_profit / profit * 100
print("Accuracy: " + str(accuracy) + "%")
# The percentage of predicted profit that would actually be made.

o_profit, o_path = optimal_path(test_graph, s, t)
print("Actual Optimal Path: " + ", ".join(o_path))
# The actual most profitable path seen in hindsight with real data from the 50
# dates.
print("Actual Optimal Profit: " + str(o_profit) + "%")
# The actual optimal profit that could have been made on said path.
performance = a_profit / o_profit * 100
print("Performance: " + str(performance) + "%")
# The profit that would have been made on the path predicted by the model as a
# percentage of the actual maximum profit that could have been made.