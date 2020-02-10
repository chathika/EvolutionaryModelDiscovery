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
from ConfigSpace.hyperparameters import UniformIntegerHyperparameter
from ConfigSpace.hyperparameters import CategoricalHyperparameter

import itertools
cs =ConfigurationSpace()
cfp = x.iloc[:,[0,-1,-2,-3]].idxmax(axis=1)
cfp_names = x.iloc[:,[0,-1,-2,-3]].columns.tolist()
cfp = cfp.apply(lambda x: cfp_names.index(x))
x = x.iloc[:,1:-3]
x["considered-farm-plots"] = cfp

for name, values in x.iteritems():
    print(name)
    if name != "considered-farm-plots":
        cs.add_hyperparameter(UniformIntegerHyperparameter(name=name,lower=values.min(),upper=values.max()))
    else:
        cs.add_hyperparameter(CategoricalHyperparameter(name=name,choices=values.unique()))


x = x.reindex(sorted(x.columns), axis=1)
f = fanova.fANOVA(x.values,y,config_space=cs)

v = viz.Visualizer(f, f.cs,".")

#v.create_all_plots(three_d=False,resolution=100)
#results = f.get_most_important_pairwise_marginals(n=13)

import math
fig, axs = plt.subplots(nrows=3,ncols=3)
idx = 0
formula=['$F_{Dist}$','$F_{Dry}$','$F_{Qual}$','$F_{Water}$','$F_{Yield}$','$F_{Mig}$','$F_{Soc}$','$F_{HAge}$','$F_{HAgri}$']
for name in x.columns:
    if name != "considered-farm-plots":
        print(name)
        df = pd.pivot_table(data[["Fitness",name]].astype({name:int}).reset_index(),columns=name,index="index",values="Fitness")
        for subname in df.columns:
            if df[subname].notna().sum() < 30:
                df = df.drop(subname,axis=1)
        bp = df.boxplot(ax=axs[math.floor(idx/3),idx%3],showfliers=False, notch=True,return_type="dict", patch_artist=True)
        for element in ['boxes','whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color="#222222")
        for patch in bp['boxes']:
            patch.set(facecolor="#AAAAAA")
        plt.setp(bp["medians"],color="#08A008",linewidth=2)
        axs[math.floor(idx/3),idx%3].title.set_text(formula[idx])
        if idx%3 != 0:
            plt.setp(axs[math.floor(idx/3),idx%3].get_yticklabels(),visible=False)
        idx += 1

plt.subplots_adjust(left  = 0.1, right =0.9, top=0.9,bottom=0.1,hspace=0.4,wspace=0.1)
fig.text(0.5, 0.02, 'Coefficient of Factor', ha='center')
fig.text(0.02, 0.5, 'Mean Squared Error', va='center', rotation='vertical')
plt.show()

allImportance = {}


from multiprocessing import pool,Process
import multiprocessing
from threading import Thread

combinations = list(itertools.combinations(list(range(x.shape[1])), 1))
'''combinations = [list(combi) for combi in combinations]
P = pool.Pool(multiprocessing.cpu_count())
def calcImportancePair(ele):
    return f.quantify_importance(ele)'''

results = []

for combi in combinations:
    results.append(f.quantify_importance(combi,quartiles=True))

df = {}

for r in results:
    for k in list(r.keys()):
        if not k in df:
            df[k] = r[k]

df=pd.DataFrame(df).T.reset_index().rename(columns={"level_0":"Factor0","level_1":"Factor1"})
df.to_csv("EMD_FANOVA_Main_Importances.csv",index=False)

#################top5#######################

def calcImportancePair(ele):
    r = f.quantify_importance(ele,quartiles=False)
    print(r)
    return r

combinations = [list(combi) for combi in  list(itertools.combinations(list(range(x.shape[1])), 1))]
for combi in combinations:
    Thread(target = calcImportancePair,args=(combi,)).start()

[print(str(r)+ str(len(f.V_U_total[r]))) for r in f.V_U_total.keys()]

combinations = [list(combi) for combi in  list(itertools.combinations(list(range(x.shape[1])), 2))]

def calcImportancePair(ele,results):
    r = f.quantify_importance(ele,quartiles=False)
    print(r)
    results.append(r)

from multiprocessing import Manager
results = Manager().list()
for combi in combinations:
    Process(target = calcImportancePair,args=(combi,results,)).start()


df = {}

for r in results:
    for k in list(r.keys()):
        if not k in df:
            df[k] = r[k]

pi = pd.DataFrame(df).T.reset_index().rename(columns={"level_0":"Factor0","level_1":"Factor1"})
pi["Factor1"]=np.where(pi["Factor1"].isnull(),pi["Factor0"],pi["Factor1"]).astype(int)
pi["Factor0"]=pi.Factor0.apply(lambda i: cs.get_hyperparameter_names()[i])
pi["Factor1"]=pi.Factor1.apply(lambda i: cs.get_hyperparameter_names()[i])
pi.to_csv("EMD_FANOVA_Pairwise_Importances.csv")
