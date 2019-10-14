# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:12:04 2019

@author: omark
"""

"""[3.1] Helper functions for use in the 3rd file."""

import networkx as nx
import pandas as pd
import math


def make_graph(filename):
    """BEHAVIOUR: Read a csv file called filename and produce a directed graph 
    with each currency-date pair as a node and edges between currencies at the
    same date and edges for each currency from each date to the next date.
    
    PRECONDITIONS: filename is a csv file in the same directory with columns 
    ds, USDEUR, USDJPY, USDGBP and USDAUD.
    
    POSTCONDITION: An nx.MultiDiGraph object is returned where each edge 
    represents the profit/loss in making the trade between the nodes that the
    edge connects. Starting at a node with x USD and going down a path with
    weight -log(k) will leave you with kx USD."""

    G = nx.MultiDiGraph()
    df = pd.read_csv(filename)
    dates = df["ds"]
    currencies = ["USDEUR", "USDJPY", "USDGBP", "USDAUD"]
    prev = "placeholder"
    for d in dates:
        for c in currencies:
            for x in currencies:
                if x == c:
                    continue
                G.add_edge(d + "  " + c, d + "  " + x, weight=-math.log(0.99))
                # Adds edge between different currencies at the same date.
                # Giving the edge 0 weight gave MemoryError with Bellman Ford.
                # 0.99 also represents some amount of USD one may lose to a
                # bid-ask spread.
            if d == "2019-05-09":
                continue
            y = float(df[df.ds == prev][c]) / float(df[df.ds == d][c])
            G.add_edge(prev + "  " + c, d + "  " + c, weight=-math.log(y))
            # Adds edge from a currency at the previously iterated date to the
            # same currency at the next date. y represents the change in value
            # faced by holding on to the currency.
        prev = d
    return G


def profit_in_specified_path(g, path):
    """BEHAVIOUR: Given a graph g and a path in that graph, return the profit
    achieved by traversing that path.
    
    PRECONDITIONS: path is a list of nodes in g and each consecutive pair of
    nodes in path are connected by an edge. Edge weights are logarithmic e.g.
    -log(k) where k is the factor by which value increases across that edge.
    
    POSTCONDITION: A float is returned which represents the profit as a
    percentage."""

    edges = [(a, b) for a, b in zip(path[:-1], path[1:])]
    length = 0
    for p, s in edges:
        weight = g[p][s][0]["weight"]
        length = length + weight
    multiplier = math.exp(-length)
    profit = multiplier * 100 - 100
    return profit


def optimal_path(g, s, t):
    """BEHAVIOUR: Given a graph g, a source date s and a target date t, find
    the path from any currency at s to any currency at t that maximises profit.
    
    PRECONDITIONS: Dates s and t are present in g with t after s. g only has
    four currencies USDEUR, USDJPY, USDGBP and USDAUD. g has nodes and edges in
    the form produced by make_graph.
    
    POSTCONDITION: Returns a float which represents the profit as a percentage
    and a list of nodes which represents the optimal path. If g has no path
    which increases value, returns 0 and an empty list."""

    currencies = ["USDEUR", "USDJPY", "USDGBP", "USDAUD"]
    length = 0
    path = []
    for c in currencies:
        for x in currencies:
            t_length, t_path = nx.single_source_bellman_ford(
                g, source=s + c, target=t + x, weight="weight"
            )
            # Our graphs can never have negative weight cycles so in theory
            # Dijsktra should work. However, nx.dijsktra is not guaranteed to
            # work for negative or float edge weights and we have both.
            if t_length < length:
                length = t_length
                path = t_path
                # Updates length and path if a more profitable path is found
                # with a different source or target.
    multiplier = math.exp(-length)
    profit = multiplier * 100 - 100
    return profit, path
