import numpy as np
import matplotlib.pyplot as plt

import ConfigSpace
import fanova
import fanova.visualizer as viz

import pandas as pd
data=pd.read_csv("FactorScores.csv")
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

#v.create_all_plots(three_d=False,resolution=10)

allImportance = {}

def calcImportancePair(pair):
    return f.quantify_importance(pair)  

from multiprocessing import pool
import multiprocessing

combinations = list(itertools.combinations(list(range(x.shape[1])), 2))
P = pool.Pool(multiprocessing.cpu_count())

results = P.map(calcImportancePair,combinations)

df = {}

for r in results:
    for k in list(r.keys()):
        if not k in df:
            df[k] = r[k]

df=pd.DataFrame(df).T.reset_index().rename(columns={"level_0":"Factor0","level_1":"Factor1"})
df.to_csv("EMD_FANOVA_Importances.csv")

