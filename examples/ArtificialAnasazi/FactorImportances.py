import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import multiprocessing

data=pd.read_csv("FactorScores.csv")
data=data[data.all_potential_farms==1]
x = data.iloc[:,4:]
x = x.iloc[:,1:-3]
y = data.iloc[:,3]


rf = RandomForestRegressor(n_estimators=100,random_state=0,n_jobs=multiprocessing.cpu_count(),bootstrap=True)
rf.fit(x.values,y.values)
#SKLean uses Gini Importance by default
fig,axs = plt.subplots(ncols=2,sharey=True)
GI = pd.DataFrame(data=[tree.feature_importances_ for tree in rf.estimators_],columns = x.columns)
GI.boxplot(ax=axs[0],vert=False)
axs[0].set_title("Gini Importance")



### Using eli5 to compute permutation accuracy importance

import eli5
from eli5.sklearn import PermutationImportance
from sklearn.feature_selection import SelectFromModel

perm = PermutationImportance(RandomForestRegressor(),cv=None,n_iter=100)
perm.fit(x.values,y.values)

PI = pd.DataFrame(data=perm.results_,columns = x.columns)
PI.boxplot(ax=axs[1],vert=False)
axs[1].set_title("Permutation Accuracy Importance")



plt.show()




from treeinterpreter import treeinterpreter as ti, utils