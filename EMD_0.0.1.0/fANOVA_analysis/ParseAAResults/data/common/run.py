#run fanova
#args: dir

import sys
#sys.path.append('/home/nguyen/Dropbox/UHasselt/fanova/fanova-master')

from pyfanova.fanova import Fanova
f=Fanova('./')
f.print_all_marginals()

from pyfanova.visualizer import Visualizer
vis = Visualizer(f)

vis.create_all_plots("./plots/")
vis.create_most_important_pairwise_marginal_plots('./plots',5)
