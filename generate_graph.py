import mosspy
import os 
import re
import sys
import csv
import requests 
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import mpl_interactions.ipyplot as iplt

class Pair:
    def __init__(self, a, b, matcha, matchb):
        self.a = a
        self.b = b
        self.matcha = matcha
        self.matchb = matchb

    def __str__(self):
        return "Match " + str(self.a) + " (" + str(self.matcha) + "%) and " + str(self.b) + " (" + str(self.matchb) + "%)"

    def __iter__(self):
        return iter([self.a, self.b, self.matcha, self.matchb])

# Create pairs of matches
pairs = []

with open('mossdata.csv', newline='') as csvfile:
    rdr = csv.reader(csvfile, delimiter=',', quotechar='|')
    rdr.__next__()
    for row in rdr:
        pair = Pair(int(row[0]), int(row[1]), int(row[2]), int(row[3]))
        pairs.append(pair)

G = nx.DiGraph()

for pair in pairs:
    if (pair.matcha > 30):
        G.add_node(pair.a)
        G.add_node(pair.b)
        c = "b"
        if (pair.matcha > 60):
            c = 'r'
        G.add_edge(pair.a, pair.b, color=c, weight=(pair.matcha - 30)/50)
    if (pair.matchb > 30):
        G.add_node(pair.a)
        G.add_node(pair.b)
        c = "b"
        if (pair.matcha > 60):
            c = 'r'
        G.add_edge(pair.b, pair.a, color=c, weight=(pair.matcha - 10)/15)


edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weight'] for u,v in edges]

fig, ax = plt.subplots()
nx.draw_circular(G, ax=ax, with_labels=True, font_weight='bold', edge_color=colors, width=weights)
plt.show()