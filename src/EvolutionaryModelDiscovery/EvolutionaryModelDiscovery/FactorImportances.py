'''EvolutionaryModelDiscovery: Automated agent rule generation and 
importance evaluation for agent-based models with Genetic Programming.
Copyright (C) 2018  Chathika Gunaratne
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
import os
import importlib
import pandas as pd
import networkx as nx
from scipy import stats
import multiprocessing
from sklearn.ensemble import RandomForestRegressor
from eli5.sklearn import PermutationImportance

from .Util import * 

class FactorImportances:

    def __init__(self, factor_scores):
        # Loading factor scores
        if isinstance(factor_scores, pd.DataFrame):
            self.factor_scores = factor_scores.fillna(0)
        elif isinstance(factor_scores, str):
            self.factor_scores = pd.read_csv(os.path.join(factor_scores)).fillna(0)
        else:
            raise TypeError("factor_scores should be a str path or pandas DataFrame.") 
        module_name = get_model_factors_module_name() 
        self.model_factors = importlib.import_module(f"EvolutionaryModelDiscovery.{module_name}")


    def train_random_forest(self, num_trees = 520, interactions = False):
        self.y = self.factor_scores["Fitness"]
        if not interactions:
            # Training random forest with first order factors (excluding interactions)
            self.x_first_order = self.factor_scores[self.model_factors.measureable_factors]
            self.rf_first_order = RandomForestRegressor(n_estimators=num_trees,random_state=0,n_jobs=multiprocessing.cpu_count(),bootstrap=False)
            self.rf_first_order.fit(self.x_first_order,self.y)
        else:
            # Training random forest with factors and factor interactions
            self.x_with_interactions = self.factor_scores[list(filter(lambda col: (col not in ["Run","Gen","Rule","Fitness"]), self.factor_scores.columns))]
            self.rf_with_interactions = RandomForestRegressor(n_estimators=num_trees,random_state=0,n_jobs=multiprocessing.cpu_count(),bootstrap=False)
            self.rf_with_interactions.fit(self.x_with_interactions,self.y)
        

    def get_trained_random_forest(self, interactions=False):
        if not interactions:
            if not hasattr(self, 'rf_first_order'):
                self.train_random_forest(interactions=False)
            rf = self.rf_first_order
        else:
            if not hasattr(self, 'rf_with_interactions'):
                self.train_random_forest(interactions=True)
            rf = self.rf_with_interactions
        return rf

    def get_gini_importances(self,interactions=False):
        rf = self.get_trained_random_forest(interactions)
        if not interactions:
            cols = self.x_first_order.columns
        else:
            cols = self.x_with_interactions.columns
        #SKLean uses Gini Importance by default
        GI = pd.DataFrame(data=[tree.feature_importances_ for tree in rf.estimators_],columns = cols)
        GI=GI[GI.sum().sort_values(ascending=True).index]
        GI = GI.loc[:,~GI.columns.duplicated()]
        return GI

    
    def get_permutation_accuracy_importances(self,interactions=False):
        rf = self.get_trained_random_forest(interactions)
        if not interactions:
            cols = self.x_first_order.columns
            features = self.x_first_order.values
        else:
            cols = self.x_with_interactions.columns
            features = self.x_with_interactions.values
        ### Using eli5 to compute permutation accuracy importance on fitted random forest
        perm = PermutationImportance(rf,cv="prefit",n_iter=10).fit(features,self.y.values)
        PI = pd.DataFrame(data=perm.results_, columns = cols)
        PI=PI[PI.sum().sort_values(ascending=True).index]
        PI = PI.loc[:,~PI.columns.duplicated()]
        return PI

    def calculate_optimal_presence_factor(self, factor, min_samples = 200, how_A_compares_to_B="less", significance=0.05, return_pvalues = False):
        presence_comparisons = []
        df = pd.pivot_table(self.factor_scores[["Fitness",factor]].astype({factor:int}).reset_index(),columns=factor,index="index",values="Fitness")
        # Only keep presence data with sufficient quantity samples
        for presence in df.columns:
            if df[presence].notna().sum() < min_samples:
                df = df.drop(presence,axis=1)
        for presence_i in df.columns:
            for presence_j in df.columns:
                statistic, pvalue = stats.mannwhitneyu(df[presence_i].dropna(),df[presence_j].dropna(),alternative=how_A_compares_to_B)
                presence_comparisons.append([presence_i,presence_j,pvalue])
        presence_comparisons = pd.DataFrame(presence_comparisons,columns=["presence_A","presence_B","pvalue_A_{}_than_B".format(how_A_compares_to_B)])
        G = nx.DiGraph()
        for i, row in presence_comparisons.iterrows():
            if row["pvalue_A_{}_than_B".format(how_A_compares_to_B)] <= (0.05 / presence_comparisons.shape[0]):
                G.add_edge(row["presence_A"],row["presence_B"], p_value = row["pvalue_A_{}_than_B".format(how_A_compares_to_B)])
        T = nx.transitive_closure(G)
        significant_differences = nx.to_pandas_adjacency(T).sum(axis=1)
        optimal_presence = significant_differences[significant_differences == significant_differences.max()].index.tolist()
        return_value = optimal_presence
        if return_pvalues:
            return_value = optimal_presence, presence_comparisons
        return return_value

                
