import sys

from pyfanova.fanova import Fanova
f=Fanova('./')
f.print_all_marginals()

import matplotlib
matplotlib.use('Agg')

from pyfanova.visualizer import Visualizer
vis=Visualizer(f)
vis.create_all_plots('./plots')
vis.create_most_important_pairwise_marginal_plots('./plots',4)
