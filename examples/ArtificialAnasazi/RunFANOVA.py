import numpy as np
import matplotlib.pyplot as plt

import ConfigSpace
import fanova
import fanova.visualizer as viz

import pandas as pd
data=pd.read_csv("examples/example_data/anasazi/FactorScores.csv")
x = data.iloc[:,4:]
y = data.iloc[:,3]

from ConfigSpace import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter

import itertools
cs =ConfigurationSpace()
for name, values in x.iteritems():
    print(name)
    cs.add_hyperparameter(UniformFloatHyperparameter(name=name,lower=values.min(),upper=values.max()))

f = fanova.fANOVA(x.values,y,config_space=cs)

v = viz.Visualizer(f, f.cs,".")

v.create_all_plots(three_d=False,resolution=10)

allImportance = {}

def calcImportancePair(pair):
    return f.quantify_importance(pair)  

from multiprocessing import pool
import multiprocessing

combinations = list(itertools.combinations(list(range(x.shape[1])), 2))
P = pool.Pool(multiprocessing.cpu_count)

results = p.map(calcImportancePair,combinations)