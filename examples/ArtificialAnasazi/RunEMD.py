import os
import sys
from EvolutionaryModelDiscovery import *
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import multiprocessing
sys.stderr = open(os.devnull, "w")  # silence stderr
from sklearn.ensemble import RandomForestRegressor
sys.stderr = sys.__stderr__
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
import eli5
from eli5.sklearn import PermutationImportance
from treeinterpreter import treeinterpreter as ti, utils
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.ticker as ticker

modelPath = "./Artificial Anasazi Ver 6.nlogo"
var = 0.05
setup = ["set harvest-adjustment (0.64 + ((" + str(2*var) + " * 0.64) * random-float 1 - (" + str(var) + " * 0.64)) )",
"set harvest-variance (0.44 + ((" + str(2*var) + " * 0.44) * random-float 1 - (" + str(var) + " * 0.44)) )",
"set base-nutrition-need (185 + ((" + str(2*var) + " * 185) * random-float 1 - (" + str(var) + " * 185)) )",
"set min-death-age (40  + ((" + str(2*var) + " * 40) * random-float 1 - (" + str(var) + " * 40)) )",
"set death-age-span (10 + ((" + str(2*var) + " * 10) * random-float 1 - (" + str(var) + " * 10)) )",
"set min-fertility-ends-age (29 + ((" + str(2*var) + " * 29) * random-float 1 - (" + str(var) + " * 29)) )",
"set fertility-ends-age-span (5 +  ((" + str(2*var) + " * 5) * random-float 1 - (" + str(var) + " * 5)) )",
"set min-fertility (0.17 + ((" + str(2*var) + " * 0.17) * random-float 1 - (" + str(var) + "  * 0.17)) )",
"set fertility-span (0.03 + ((" + str(2*var) + " * 0.03) * random-float 1 - (" + str(var) + "  * 0.03)) )",
"set maize-gift-to-child (0.47 + ((" + str(2*var) + " * 0.47) * random-float 1 - (" + str(var) + "  * 0.47)) )",
"set water-source-distance (11.5  + ((" + str(2*var) + " * 11.5) * random-float 1 - (" + str(var) + "  * 11.5)) )",
'setup']
measurements = ["L2-error"]
ticks = 550
emd = EvolutionaryModelDiscovery("/opt/netlogo/", modelPath,setup, measurements, ticks)
emd.setMutationRate(0.1)
emd.setCrossoverRate(0.8)
emd.setGenerations(2)
emd.setReplications(20)
emd.setDepth(4,10)
emd.setPopulationSize(5)
emd.setIsMinimize(True)
def cindexObjective(results):
    #print(results.iloc[-1][0])
    return (results.iloc[-1][0])

emd.setObjectiveFunction(cindexObjective)

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    emd.evolve()
    
    SMALL_SIZE = 22
    MEDIUM_SIZE = 34
    BIGGER_SIZE = 28
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rcParams['figure.dpi'] = 72
    plt.rcParams["font.weight"] = "medium"
    plt.rcParams["font.family"] = "sansserif"
    plt.rcParams["text.color"] = "black"
    plt.rcParams["axes.labelweight"] = "medium"
    plt.rcParams['axes.linewidth'] = 0.1

    data=pd.read_csv("FactorScores.csv")
    data=data[data.all_potential_farms==1]
    factor_names=['compare_distance', 'compare_dryness', 'compare_quality','compare_water_availability', 'compare_yeild', 'desire_migration','desire_social_presence', 'homophily_age','homophily_agricultural_productivity']
    x = data[factor_names]
    y = data["Fitness"]
    fig, axs = plt.subplots(nrows=3,ncols=3)
    idx = 0
    sample_size=200
    formula=['$F_{Dist}$','$F_{Dry}$','$F_{Qual}$','$F_{Water}$','$F_{Yield}$','$F_{Mig}$','$F_{Soc}$','$F_{HAge}$','$F_{HAgri}$']
    for name in x.columns:
        if name != "considered-farm-plots":
            print(name)
            df = pd.pivot_table(data[["Fitness",name]].astype({name:int}).reset_index(),columns=name,index="index",values="Fitness")
            for subname in df.columns:
                if df[subname].notna().sum() < sample_size:
                    df = df.drop(subname,axis=1)#
                #elif df[subname].notna().sum() > sample_size:
                    #df1 = df[df[subname].notna()].sample((df[subname].notna().sum()-sample_size))
                    #print(df[subname].notna().sum())
                    #df = df[~df.index.isin(df1.index)]
            bp = df.boxplot(ax=axs[math.floor(idx/3),idx%3],showfliers=False, showmeans=False, notch=True,return_type="dict", patch_artist=True)
            for element in ['boxes','whiskers', 'fliers', 'means', 'medians', 'caps']:
                plt.setp(bp[element], color="black",linewidth=2)
            for patch in bp['boxes']:
                patch.set(facecolor="silver")
            plt.setp(bp["medians"],color="dodgerblue",linewidth=5)
            plt.setp(bp["means"],color="dodgerblue",linewidth=5)
            plt.setp(bp["whiskers"],color="black",linewidth=3)
            plt.setp(bp["caps"],color="black",linewidth=3)
            axs[math.floor(idx/3),idx%3].grid(None)
            axs[math.floor(idx/3),idx%3].set_title(formula[idx],pad=15,fontdict={"fontsize":28,"fontweight":"roman"})
            if idx%3 != 0:
                plt.setp(axs[math.floor(idx/3),idx%3].get_yticklabels(),visible=False)
            idx += 1

    plt.subplots_adjust(left  = 0.1, right =0.9, top=0.9,bottom=0.1,hspace=0.4,wspace=0.1)
    fig.text(0.5, 0.02, 'Factor Presence', ha='center',fontsize=32)
    fig.text(0.02, 0.5, 'Root Mean Squared Error', va='center', rotation='vertical',fontsize=32)
    plt.show()
    ####################################
    #Figure out best number of tree for random forest
    #Do a train test split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.01, random_state=0)
    #Fit random forest to data. 
    oob_scores = []
    all_predictions = []
    num_trees = list(range(10,1000,10))
    for n in num_trees:
        rf = RandomForestRegressor(n_estimators=n,random_state=0,n_jobs=multiprocessing.cpu_count(),bootstrap=True,oob_score=True)
        rf.fit(X_train,y_train)
        oob_scores.append(rf.oob_score_)
        predictions = rf.predict(X_test)
        all_predictions.append(np.array(predictions))
    preds = []
    for pred in all_predictions:
        preds.append(np.mean( np.abs(pred-y_test) / y_test) )
    
    ax=pd.DataFrame(data=[num_trees,preds]).T.rename({0:"Number of Trees",1: "Mean Percentage Error"},axis=1).plot("Number of Trees","Mean Percentage Error",kind="scatter",color="black")
    vals = ax.get_yticks()
    ax.set_ylim(0.2875,0.2925)
    ax.set_yticklabels(["{:,.2%}".format(i) for i in vals])
    plt.show()
    ##########################################
    n=520
    rf = RandomForestRegressor(n_estimators=n,random_state=0,n_jobs=multiprocessing.cpu_count(),bootstrap=False)
    rf.fit(x,y)
    #SKLean uses Gini Importance by default
    GI = pd.DataFrame(data=[tree.feature_importances_ for tree in rf.estimators_],columns = x.columns)
    ### Using eli5 to compute permutation accuracy importance on fitted random forest
    perm = PermutationImportance(rf,cv="prefit",n_iter=10).fit(x.values,y.values)
    # Permutation Accuracy Importance
    PI = pd.DataFrame(data=perm.results_,columns = x.columns)
    #Rename columns to conform to formulae used in paper
    formula={'considered-farm-plots':"$S$", 'compare_quality':'$F_{Qual}$', 'compare_distance':'$F_{Dist}$','homophily_age':'$F_{HAge}$', 'desire_migration':'$F_{Mig}$', 'compare_yeild':'$F_{Yield}$',
    'homophily_agricultural_productivity':'$F_{HAgri}$', 'compare_dryness':'$F_{Dry}$','compare_water_availability':'$F_{Water}$', 'desire_social_presence':'$F_{Soc}$'}
    PI.columns = [formula[col] for col in PI.columns]
    GI.columns = [formula[col] for col in GI.columns]
    PI=PI[PI.sum().sort_values(ascending=True).index]
    GI=GI[PI.sum().sort_values(ascending=True).index]
    #Generate Main Effects plot
    fig,axs = plt.subplots(ncols=2)
    bps = []
    bp = GI.boxplot(ax=axs[0],vert=False, notch=True,return_type="dict", patch_artist=True)
    axs[0].set_title("Gini Importance",fontdict={"fontweight":"roman"},pad=15)
    bps.append(bp)
    bp = PI.boxplot(ax=axs[1],vert=False, notch=False,return_type="dict", patch_artist=True)
    axs[1].set_title("Permutation Accuracy Importance",fontdict={"fontweight":"roman"},pad=15)
    bps.append(bp)
    for bpi in bps:
        for element in ['boxes','whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bpi[element], color="black")
        for patch in bpi['boxes']:
            patch.set(facecolor="silver")    
        plt.setp(bpi["medians"],color="dodgerblue",linewidth=2)

    axs[0].set_xlim(0,0.4)
    axs[1].set_xlim(0,0.4)
    axs[0].grid(None)
    axs[0].invert_xaxis()
    axs[0].yaxis.tick_right()
    #axs[0].set_yticks(axs[0].get_yticks,[])
    axs[1].grid(None)
    axs[0].tick_params(axis='y',labelright='off')
    axs[1].tick_params(axis='y', which='major', pad=50)
    for label in axs[1].get_yticklabels():
        label.set_horizontalalignment('center')
        label.set_fontweight("bold")
        label.set_fontsize(28)

    plt.show()
    ##################Joint Contributions Plot############
    data_sorted = data.sort_values("Fitness")
    factors = x.columns.tolist()
    data_sorted = data_sorted[factors].join(data_sorted["Fitness"]).sort_values("Fitness")
    x_sorted = data_sorted.iloc[:,:-1]
    y_sorted = data_sorted.iloc[:,-1]
    ds1 = x_sorted.values
    print (np.mean(rf.predict(ds1)))
    prediction1, bias1, contributions1 = ti.predict(rf, ds1, joint_contribution=True)
    aggregated_contributions1 = utils.aggregated_contribution(contributions1)
    res = []
    for k in set(aggregated_contributions1.keys()):
        if len(k) <=3 :
            res.append(([x.columns.tolist()[index] for index in k] , aggregated_contributions1.get(k, 0)))   

    IE = pd.DataFrame(res)
    IE.columns = ["Interaction","Contribution"]
    IE["Contribution"]  = IE.Contribution.apply(lambda k: k[0]).abs()
    IE["Contribution"] = IE["Contribution"]/IE["Contribution"].max()
    IE["Interaction"] = IE["Interaction"].apply(lambda key: str(list([formula[f] for f in key])))
    IE = IE.sort_values(by="Contribution")
    TopIE = IE[-20:]
    ax = TopIE.plot("Interaction","Contribution",kind="barh",legend = None,width=0.7,color="royalblue")
    vals = ax.get_yticklabels()
    ax.set_yticklabels([i.get_text().replace("[","{").replace("]","}") for i in vals],fontsize28)
    ax.set_xlabel("Normalized Contribution to Random Forest Prediction",labelpad=15,fontsize=SMALL_SIZE)
    ax.set_ylabel("Factor Interaction",labelpad=15,fontsize=(SMALL_SIZE + 2))
    plt.show()
    #########################
    #Statistical test comparing PI
    mwu = []
    for A in PI.columns:
        mwu_A = []
        for B in PI.columns:
            statistic, pvalue = stats.mannwhitneyu(PI[A].dropna(),PI[B].dropna(),alternative="greater")
            mwu_A.append(pvalue)
            if pvalue < 0.05:
                print(str(A) + " > " + str(B))
        mwu.append(mwu_A)

    mwu=pd.DataFrame(mwu,columns=PI.columns,index=PI.columns).iloc[::-1]
    flatui=["mediumaquamarine","gainsboro"]
    sns.palplot(sns.color_palette(flatui))
    ax = sns.heatmap(mwu, annot=True, linewidth=2,linecolor="black",center=0.05,cmap=sns.color_palette(flatui), fmt=".1e",cbar=None, annot_kws={"color": "black","size":16},xticklabels=1,yticklabels=1)
    ax.set_xlabel("B",fontsize=28,labelpad=10)
    ax.set_ylabel("A",fontsize=28,labelpad=10)
    ax.tick_params(axis = 'both', which = 'major', labelsize = 28)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top') 
    plt.show()
    #########################
    #Plot progress of GP Runs
    #Plotting cumulative minimum of the mean fitness of rules by generation for each GP run
    gp_progress = pd.pivot_table(pd.read_csv("FactorScores.csv")[["Run","Gen","Rule","Fitness"]].groupby(["Run","Gen","Rule"]).apply(lambda x: x.mean()),columns="Run",index="Gen",values="Fitness",aggfunc=np.min).apply(lambda x: x.cummin(),axis=0)
    gp_progress.columns = gp_progress.columns.astype(int)
    fig, ax = plt.subplots()
    gp_progress.plot(ax=ax)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Mean fitness of best so far")
    ax.legend(loc='upper center', bbox_to_anchor=(0.7, 1.05),ncol=5,fancybox=True, framealpha=1, shadow=True, borderpad=1,title="Run")
    plt.show()
    ################Find Best Values for Dryness, Quality, Social Presence, and Migration####################
    fitness_comparisons = {}
    formula={'considered-farm-plots':"$S$", 'compare_quality':'$F_{Qual}$', 'compare_distance':'$F_{Dist}$','homophily_age':'$F_{HAge}$', 'desire_migration':'$F_{Mig}$', 'compare_yeild':'$F_{Yield}$',
    'homophily_agricultural_productivity':'$F_{HAgri}$', 'compare_dryness':'$F_{Dry}$','compare_water_availability':'$F_{Water}$', 'desire_social_presence':'$F_{Soc}$'}
    for name in x.columns:
        if name != "considered-farm-plots":
            print(name)
            fitness_comparisons[name] = []
            df = pd.pivot_table(data[["Fitness",name]].astype({name:int}).reset_index(),columns=name,index="index",values="Fitness")
            print(df.head())
            for subname in df.columns:
                if df[subname].notna().sum() < 200:
                    df = df.drop(subname,axis=1)
            for val_i in df.columns:
                for val_j in df.columns:
                    statistic, pvalue = stats.mannwhitneyu(df[val_i].dropna(),df[val_j].dropna(),alternative="less")
                    fitness_comparisons[name].append([val_i,val_j,pvalue])
                    if pvalue < 0.05:
                        print(str(val_i) + " < " + str(val_j))

    gs = gridspec.GridSpec(2, 6)
    axs=[]
    axs.append(plt.subplot(gs[0, 0:2]))
    axs.append(plt.subplot(gs[0,2:4]))
    axs.append(plt.subplot(gs[0,4:6]))
    axs.append(plt.subplot(gs[1,1:3]))
    axs.append(plt.subplot(gs[1,3:5]))
    flatui=["mediumaquamarine","gainsboro"]
    fig = plt.gcf()
    for idx, col in enumerate(["compare_quality","desire_social_presence","desire_migration","compare_dryness","compare_distance"]):#x.columns:
        fitness_comparisons_i = pd.pivot_table(pd.DataFrame(fitness_comparisons[col],columns=["A","B","pvalue"]),columns = "B",index="A",values="pvalue")
        ax = sns.heatmap(fitness_comparisons_i, annot=True, linewidth=2,linecolor="black",center=0.05,cmap=sns.color_palette(flatui), fmt=".1e",cbar=None, annot_kws={"color": "black","size":11 + (2 * 6 - fitness_comparisons_i.columns.size)},ax=axs[idx],xticklabels = 1,yticklabels=1)
        ax.set_title(formula[col],fontsize=30,pad=15)
        ax.set_xlabel("B",fontsize=20,labelpad=10)
        ax.set_ylabel("A",fontsize=20,labelpad=10)
        ax.tick_params(axis = 'both', which = 'both', labelsize = 20)
        ax.set_yticklabels(ax.get_yticklabels(), rotation = 0)
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 0)

    plt.show()
    #######################################
    labs=["desire_social_presence","desire_migration"]
    considered_labs=[]
    for xlab in ["compare_quality"]:
        fig,axs = plt.subplots(ncols=2)
        for idy,ylab in enumerate(labs):
            labs_i=[xlab,ylab]
            labs_i.sort()
            if xlab!=ylab and (labs_i not in considered_labs):
                considered_labs.append(labs_i)
                print(considered_labs)
                hm_counts=pd.pivot_table(data[[xlab,ylab,"Fitness"]],columns=xlab,index=ylab,values="Fitness",aggfunc=lambda x: x.shape[0])
                hm_counts=hm_counts.apply(lambda x: x.apply(lambda y: 1 if y >=1 else np.nan))
                hm_data=pd.pivot_table(data[[xlab,ylab,"Fitness"]],columns=xlab,index=ylab,values="Fitness",aggfunc=np.median)
                hm_data=(hm_counts*hm_data).round(0)#.astype(int)
                hm_data.columns=hm_data.columns.astype(int)
                hm_data.index=hm_data.index.astype(int)            
                ax=sns.heatmap(hm_data, annot=True,fmt=".0f", vmin=900, vmax=3000, annot_kws={"color": "white","size":12},cbar_kws={'label': 'Median Fitness'},ax=axs[idy])
                ax.figure.axes[-1].yaxis.label.set_size(20)
                ax.figure.axes[-1].tick_params(labelsize=20)
                ax.set_xlabel(formula[xlab],fontsize=24)
                ax.set_ylabel(formula[ylab],fontsize=24)

    plt.show()
    ############################
    ax=sns.boxplot(data=data.sort_values("Fitness").head(25)[factor_names].rename(formula,axis=1),orient="h", color="#AAAAAA")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    # iterate over boxes
    for i,box in enumerate(ax.artists):
        box.set_edgecolor('black')
        box.set_facecolor('#AAAAAA')
        # iterate over whiskers and median lines
        ax.lines[range(6*i,6*(i+1))[-2]].set_color('#08A008') #['boxes','whiskers', 'fliers', 'means', 'medians', 'caps']
        ax.lines[range(6*i,6*(i+1))[-2]].set_linewidth(3)

    ax.set_xlabel("Coefficient of Factor",fontsize=24)
    plt.show()
    #################Plot Best Models#############
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}',  r'\usepackage{helvet}', r'\usepackage{sansmath}', r'\sansmath',r'\newcommand{\opA}{\mathop{\vphantom{\sum}\mathchoice{\vcenter{\hbox{\Huge \textsf{argmax}}}}{\vcenter{\hbox{\Huge argmax}}}{\mathrm{\textsf{argmax}}}{\mathrm{\textsf{argmax}}}}\displaylimits}']
    plt.rcParams["font.weight"] = "medium"
    plt.rcParams["font.family"] = "sansserif"
    plt.rcParams["text.color"] = "black"
    plt.rcParams["axes.labelweight"] = "medium"
    plt.rcParams['figure.dpi'] = 72
    plt.rcParams["font.weight"] = "medium"
    plt.rcParams["font.family"] = "sansserif"
    plt.rcParams["text.color"] = "black"
    plt.rcParams["axes.labelweight"] = "medium"
    qual=pd.read_csv("3Qual/Artificial Anasazi Ver 6 3Qual-table.csv")
    dist=pd.read_csv("Dist/Artificial Anasazi Ver 6 Dist-table.csv")
    mig3qual5=pd.read_csv("3Mig5Qual/Artificial Anasazi Ver 6 3Mig5Qual-table.csv")
    soc5qual6=pd.read_csv("5Soc6Qual/Artificial Anasazi Ver 6 5Soc6Qual-table.csv")
    qual["Rule"]="$\displaystyle \opA_{x \in S_{All}} (F_{Qual})$"
    dist["Rule"]="$\displaystyle \opA_{x \in S_{All}} (-F_{Dist})$"
    mig3qual5["Rule"]="$\displaystyle \opA_{x \in S_{All}} (3*F_{Mig}+5*F_{Qual})$"
    soc5qual6["Rule"]="$\displaystyle \opA_{x \in S_{All}} (5*F_{Soc}+6*F_{Qual})$"
    rundata=qual.append(dist).append(mig3qual5).append(soc5qual6)
    rundata=rundata[rundata.Step==551]
    bp = rundata.boxplot("L2_error",by="Rule",showfliers=False, showmeans=False, notch=False,return_type="dict", patch_artist=True,vert=False)
    for element in ['boxes','whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp.L2_error[element], color="black",linewidth=4)

    for patch in bp.L2_error['boxes']:
        patch.set(facecolor="silver")

    plt.setp(bp.L2_error["medians"],color="dodgerblue",linewidth=5)
    plt.yticks(fontsize=36)
    plt.xticks(fontsize=32)
    plt.ylabel("")
    plt.xlabel(r"\textsf{Root Mean Squared Error}",labelpad=15)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.tick_params(axis='x', which='major', pad=15)
    plt.title("")
    plt.suptitle("")
    plt.grid(None)
    plt.show()
    ###################################
    df = pd.pivot_table(rundata.reset_index(),columns=["Rule"],values="L2_error",index="index")
    S_pvals=[]
    for A in df:
        mwu_A = []
        for B in df:
            statistic, pvalue = stats.mannwhitneyu(df[A].dropna(),df[B].dropna(),alternative="less")
            mwu_A.append(pvalue)
        S_pvals.append(mwu_A)

    pd.DataFrame(S_pvals,columns=df.columns,index=df.columns)
    #################
    ddf=pd.read_csv("FactorScores.csv")[["Fitness","all_potential_farms","potential_family_farms","potential_farms_near_best_performers","potential_neighborhood_farms"]]
    ddf=ddf.apply(lambda x: x.iloc[1:].apply(lambda y: x.iloc[0] if y==1 else np.nan),axis=1)
    ddf.columns=['$S_{All}$', '$S_{Fam}$', '$S_{Perf}$', '$S_{Neigh}$']
    fig,ax = plt.subplots()
    bp = ddf.boxplot(showfliers=False, showmeans=False, notch=False,return_type="dict", patch_artist=True,vert=False)
    for element in ['boxes','whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color="black", linewidth=4)

    for patch in bp['boxes']:
        patch.set(facecolor="silver")

    plt.setp(bp["medians"],color="dodgerblue",linewidth=5)
    plt.yticks(fontsize=26)
    plt.xticks(fontsize=24)
    plt.ylabel("")
    plt.xlabel("Root Mean Squared Error",labelpad=15,fontweight="roman",fontfamily="sansserif",fontsize=24)
    plt.title("")
    plt.grid(None)
    plt.suptitle("")
    plt.show()

