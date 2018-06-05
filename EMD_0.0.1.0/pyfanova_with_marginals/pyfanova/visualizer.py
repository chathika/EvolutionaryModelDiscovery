import os
import numpy as np
import matplotlib as mpl
import random

mpl.use('Agg') #NGUYEN: add this for running this file through out ssh 

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import gca


class Visualizer(object):

    #NGUYEN: add this
    file_format = ['png','eps'][0]
    text_size = 15
    x_axis_title = ['True','False'][1]
    alpha = 0.4 # opaque
    savingOutput = True

    def get_random_color(self,pastel_factor = 0.5):
        return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

    def color_distance(self,c1,c2):
        return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

    def generate_new_color(self,existing_colors,pastel_factor = 0.5):
        max_distance = None
        best_color = None
        for i in range(0,100):
            color = self.get_random_color(pastel_factor = pastel_factor)
            if not existing_colors:
                return color
            best_distance = min([self.color_distance(color,c) for c in existing_colors])
            if not max_distance or best_distance > max_distance:
                max_distance = best_distance
            best_color = color
        return best_color

    def __init__(self, fanova):
        self._fanova = fanova
        mpl.rcParams['axes.titlesize'] = 'large'
        mpl.rcParams['axes.labelsize'] = 'large'

    def create_all_plots(self, directory, **kwargs):
        """
            Create plots for all main effects.
        """
        assert os.path.exists(directory), "directory %s doesn't exist" % directory
        
        #categorical parameters
        for param_name in self._fanova.get_config_space().get_categorical_parameters():
            plt.clf()
            outfile_name = os.path.join(directory, param_name.replace(os.sep, "_") + "." + self.file_format) #NGUYEN: add file_format
            print("creating %s" % outfile_name)
            self.plot_categorical_marginal(param_name,directory)
            plt.savefig(outfile_name, format = self.file_format, bbox_inches='tight') #NGUYEN: add the last two params

        #continuous and integer parameters
        params_to_plot = []
        params_to_plot.extend(self._fanova.get_config_space().get_continuous_parameters())
        params_to_plot.extend(self._fanova.get_config_space().get_integer_parameters())
        for param_name in params_to_plot:
            plt.clf()
            outfile_name = os.path.join(directory, param_name.replace(os.sep, "_") + "." + self.file_format) #NGUYEN: add file_format
            print("creating %s" % outfile_name)
            self.plot_marginal(param_name, directory)
            plt.savefig(outfile_name, format = self.file_format, bbox_inches='tight') #NGUYEN: add the last two params

    def create_most_important_pairwise_marginal_plots(self, directory, n=20):
        categorical_parameters = self._fanova.get_config_space().get_categorical_parameters()

        most_important_pairwise_marginals = self._fanova.get_most_important_pairwise_marginals(n)

        print(most_important_pairwise_marginals)
        
        for param1, param2 in most_important_pairwise_marginals:
            #NGUYEN
            if ((param1 in categorical_parameters) and (param2 not in categorical_parameters)) or ((param1 not in categorical_parameters) and (param2 in categorical_parameters)):
                self.NGUYEN_plot_pairwise_marginal_oneCat_onePlot(directory, param1, param2)
            if ((param1 in categorical_parameters) and (param2 in categorical_parameters)): # TODO: this plot looks ugly now
                self.NGUYEN_plot_pairwise_marginal_twoCats(directory, param1, param2)
            
            if param1 in categorical_parameters or param2 in categorical_parameters:
                #print("skipping pairwise marginal plot %s x %s, because one of them is categorical" % (param1, param2))
                continue
                
            if param1 not in categorical_parameters and param2 not in categorical_parameters:
                outfile_name = os.path.join(directory, param1.replace(os.sep, "_") + "x" + param2.replace(os.sep, "_") + '.' + self.file_format)
                plt.clf()
                self.plot_pairwise_marginal(param1, param2)
                print("creating %s" % outfile_name)
                plt.savefig(outfile_name)
            
   
    def plot_categorical_marginal(self, param, directory):
        
        #NGUYEN: add two args: text_size and x_axis_title
        
        threshold_for_wrap_xtick = 5 # NGUYEN: if there is any xtick having length >= this value, xtick will be rotated
        rotation_for_wrap_xtick = 45
        
        if isinstance(param, int):
            dim = param
            param_name = self._fanova.get_parameter_names()[dim]
        else:
            if param not in self._fanova.param_name2dmin:
                print("Parameter %s not known" % param)
                return
            dim = self._fanova.param_name2dmin[param]
            param_name = param

        categorical_size = self._fanova.get_config_space().get_categorical_size(param_name)

        labels = self._fanova.get_config_space().get_categorical_values(param)
        
        #NGUYEN: add this for wrapping xticks
        rotate_xtick = False
        for label in labels:
            if len(label) > threshold_for_wrap_xtick:
                rotate_xtick = True
                break
        
        if param_name not in self._fanova.get_config_space().get_categorical_parameters():
            print("Parameter %s is not a categorical parameter!" % (param_name))

        indices = np.asarray(list(range(categorical_size)))
        width = 0.5
        marginals = [self._fanova.get_categorical_marginal_for_value(param_name, i) for i in range(categorical_size)]
        mean, std = list(zip(*marginals))
        #plt.bar(indices, mean, width, color='red', yerr=std)
        #plot mean
        b = plt.boxplot([[x] for x in mean], 0, '', labels=labels)
        if rotate_xtick:
            print('rotating')
            gca().set_xticklabels(labels, rotation=rotation_for_wrap_xtick, ha="right")
            plt.setp(gca().get_xticklabels(), fontsize=self.text_size)
            plt.setp(gca().get_yticklabels(), fontsize=self.text_size)
            #rotation_for_wrap_xtick
             #.set_xticklabels(labels, rotation=rotation_for_wrap_xtick, ha="right")

        # save output to text file
        split = ' '
        lsOut = [param_name, split.join(labels), split.join([str(x) for x in mean]), split.join([str(x) for x in std])]
        if self.savingOutput:
            outTextFile = directory + '/' + param_name + '.png.txt'
            print('saving to ' + outTextFile)
            with open(outTextFile, 'wt') as f:
                f.write('\n'.join(lsOut))
        
        min_y = mean[0]
        max_y = mean[0]
        # blow up boxes 
        for box, std_ in zip(b["boxes"], std):
            y = box.get_ydata()
            y[2:4] = y[2:4] + std_
            y[0:2] = y[0:2] - std_
            y[4] = y[4] - std_
            box.set_ydata(y)
            min_y = min(min_y, y[0] - std_)
            max_y = max(max_y, y[2] + std_)
        
        plt.ylim([min_y, max_y])
        
        #plt.xticks(indices, labels)
        plt.ylabel("Cost", fontsize = self.text_size)
        if self.x_axis_title == True:
            plt.xlabel(param_name)
        plt.tight_layout()

        return plt

    def _check_param(self, param):
        if isinstance(param, int):
            dim = param
            param_name = self._fanova.get_parameter_names()[dim]
        else:
            assert param in self._fanova.param_name2dmin, "param %s not known" % param
            dim = self._fanova.param_name2dmin[param]
            param_name = param

        return (dim, param_name)

    #NGUYEN: in case one of the two params is categorical, print multi-plots, one for each value of that parameter
    def NGUYEN_plot_pairwise_marginal_oneCat_seperatedPlots(self, directory, param_1, param_2, lower_bound_1=0, upper_bound_1=1, lower_bound_2=0, upper_bound_2=1, resolution=20):

        dim1, param_name_1 = self._check_param(param_1)
        dim2, param_name_2 = self._check_param(param_2)    
        
        # if there is any categorical parameter, it must be param_2
        if param_name_1 in self._fanova.get_config_space().get_categorical_parameters():
            temp_dim = dim1
            temp_param_name = param_name_1
            dim1 = dim2
            param_name_1 = param_name_2
            dim2 = temp_dim
            param_name_2 = temp_param_name
        
        # here is what I am adding
        if (param_name_1 not in self._fanova.get_config_space().get_categorical_parameters()) and (param_name_2 in self._fanova.get_config_space().get_categorical_parameters()):
            # do something
            resolution = 100
            print(resolution)
            ls_categorical_vals = self._fanova.get_config_space().get_categorical_values(param_name_2)
            categorical_size = self._fanova.get_config_space().get_categorical_size(param_name_2)
            for categorical_id in range(categorical_size):
                categorical_val = ls_categorical_vals[categorical_id]
                grid = np.linspace(lower_bound_1, upper_bound_1, resolution)
                display_grid = [self._fanova.unormalize_value(param_name_1, value) for value in grid]
                mean = np.zeros(resolution)
                std = np.zeros(resolution)
                for i in range(0, resolution):
                    (m, s) = self._fanova._get_marginal_for_value_pair(dim1, dim2, grid[i], categorical_id)
                    mean[i] = m
                    std[i] = s
                mean = np.asarray(mean)
                std = np.asarray(std)
                lower_curve = mean - std
                upper_curve = mean + std
                plt.clf()
                plt.plot(display_grid, mean, 'b')
                plt.fill_between(display_grid, upper_curve, lower_curve, facecolor='red', alpha=self.alpha)
                plt.setp(gca().get_xticklabels(), fontsize=self.text_size)
                plt.setp(gca().get_yticklabels(), fontsize=self.text_size)
                plt.xlabel(categorical_val, fontsize=self.text_size)
                plt.ylabel("Cost", fontsize=self.text_size)
                outfile_name = os.path.join(directory, param_name_1.replace(os.sep, "_") + "x" + param_name_2.replace(os.sep, "_") + "x" + categorical_val + '.' + self.file_format)
                print("creating %s" % outfile_name)
                plt.savefig(outfile_name)
    
    #NGUYEN: in case one of the two params is categorical, print one plots, each curve in the plot is for one value of the categorical param
    def NGUYEN_plot_pairwise_marginal_oneCat_onePlot(self, directory, param_1, param_2, lower_bound_1=0, upper_bound_1=1, lower_bound_2=0, upper_bound_2=1, resolution=20):

        print("NGUYEN_plot_pairwise_marginal_oneCat_onePlot")

        dim1, param_name_1 = self._check_param(param_1)
        dim2, param_name_2 = self._check_param(param_2)    
             
        # if there is any categorical parameter, it must be param_2
        if param_name_1 in self._fanova.get_config_space().get_categorical_parameters():
            temp = param_1
            param_1 = param_2
            param_2 = temp
            dim1, param_name_1 = self._check_param(param_1)
            dim2, param_name_2 = self._check_param(param_2)
            
            print(dim1, dim2)
        
        # save values in text file
        split = ' '
        lsOut = [split.join([param_name_1,param_name_2])]
        
        if (param_name_1 not in self._fanova.get_config_space().get_categorical_parameters()) and (param_name_2 in self._fanova.get_config_space().get_categorical_parameters()):
            # do something
            ls_categorical_vals = self._fanova.get_config_space().get_categorical_values(param_name_2)
            categorical_size = self._fanova.get_config_space().get_categorical_size(param_name_2)
            plt.clf()
            ls_colors=['red','green','blue','yellow','black','cyan','magenta']
            if categorical_size > len(ls_colors):
                ls_colors = []
                for i in range(0,categorical_size):
                    ls_colors.append(self.generate_new_color(ls_colors))	
            color_id=0

            grid = np.linspace(0, 1, resolution)
            display_grid = [self._fanova.unormalize_value(param_name_1, value) for value in grid]

            lsOut.append(split.join([str(i) for i in display_grid]))
            lsOut.append(split.join([str(i) for i in ls_categorical_vals]))

            for categorical_id in range(categorical_size):
                categorical_val = ls_categorical_vals[categorical_id]
                mean = np.zeros(resolution)
                std = np.zeros(resolution)
                for i in range(0, resolution):
                    (m, s) = self._fanova._get_marginal_for_value_pair(dim1, dim2, grid[i], categorical_id)
                    mean[i] = m
                    std[i] = s
                mean = np.asarray(mean)
                std = np.asarray(std)
                lower_curve = mean - std
                upper_curve = mean + std
                legend_label = param_name_2 + ' = ' + categorical_val
                plt.plot(display_grid, mean, ls_colors[color_id], label=legend_label)
                plt.fill_between(display_grid, upper_curve, lower_curve, facecolor=ls_colors[color_id], alpha=self.alpha)
                color_id=color_id+1
                
                # save output values as text
                lsOut.append(split.join([categorical_val,
                            split.join([str(i) for i in mean]),
                            split.join([str(i) for i in std])]))

            outfile_name = os.path.join(directory, param_name_1.replace(os.sep, "_") + "x" + param_name_2.replace(os.sep, "_") + "." + self.file_format)
            print("creating %s" % outfile_name)
            plt.setp(gca().get_xticklabels(), fontsize=self.text_size)
            plt.setp(gca().get_yticklabels(), fontsize=self.text_size)
            plt.xlabel(param_1, fontsize=self.text_size)
            plt.ylabel("Cost", fontsize=self.text_size)
            #plt.legend()
            lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=1, prop={'size':self.text_size})
            plt.savefig(outfile_name,bbox_extra_artists=(lgd,), bbox_inches='tight')

            # saving output to text files (for further plotting)
            if self.savingOutput:
                outTextFile = outfile_name + '.txt'
                with open(outTextFile, 'wt') as f:
                    f.write('\n'.join(lsOut))


            
    def NGUYEN_plot_pairwise_marginal_twoCats(self, directory, param_1, param_2, lower_bound_1=0, upper_bound_1=1, lower_bound_2=0, upper_bound_2=1, resolution=20):
		# NGUYEN: does it work if there are conditioinal parameters?

        # swap params, the one with more values will be the first one
        swap = True
        if swap:
            dim1, param_name_1 = self._check_param(param_1)
            dim2, param_name_2 = self._check_param(param_2)
            ls_categorical_vals_1 = self._fanova.get_config_space().get_categorical_values(param_name_1)
            ls_categorical_vals_2 = self._fanova.get_config_space().get_categorical_values(param_name_2)
            if len(ls_categorical_vals_1)<len(ls_categorical_vals_2):
                temp=param_1
                param_1=param_2
                param_2=temp

        dim1, param_name_1 = self._check_param(param_1)
        dim2, param_name_2 = self._check_param(param_2)    

        # save values in text file
        split = ' '
        lsOut = [split.join([param_name_1,param_name_2])]
        
        if (param_name_1 in self._fanova.get_config_space().get_categorical_parameters()) and (param_name_2 in self._fanova.get_config_space().get_categorical_parameters()):
            # do something
            plt.clf()
            ls_categorical_vals_1 = self._fanova.get_config_space().get_categorical_values(param_name_1)
            ls_categorical_vals_2 = self._fanova.get_config_space().get_categorical_values(param_name_2)
            lsOut.append(split.join(ls_categorical_vals_1))
            lsOut.append(split.join(ls_categorical_vals_2))
            n_val1 = len(ls_categorical_vals_1)
            ls_colors=['red','green','blue','yellow','black','cyan','magenta']
            color_id=0
            for categorical_val_2_id in range(0,len(ls_categorical_vals_2)):
                categorical_val_2 = ls_categorical_vals_2[categorical_val_2_id]
                mean = np.zeros(n_val1)
                std = np.zeros(n_val1)
                for i in range(0, n_val1):
                    (m, s) = self._fanova._get_marginal_for_value_pair(dim1, dim2, i, categorical_val_2_id)
                    mean[i] = m
                    std[i] = s
                mean = np.asarray(mean)
                std = np.asarray(std)
                print(mean)
                print(std)
                #plt.errorbar(np.arange(n_val1), mean, std, fmt = 'ok', ecolor=ls_colors[color_id], capthick=5, label = categorical_val_2)
                legend_label = param_name_2 + ' = ' + categorical_val_2
                plt.errorbar(np.arange(n_val1), mean, std, fmt = '.', color = 'black', markersize = 5, elinewidth = 5, ecolor=ls_colors[color_id], capthick=1, label = legend_label)
                color_id=color_id+1
                lsOut.append(split.join([categorical_val_2, split.join([str(x) for x in mean]), split.join([str(x) for x in std])]))
            outfile_name = os.path.join(directory, param_name_1.replace(os.sep, "_") + "x" + param_name_2.replace(os.sep, "_") + "." + self.file_format)
            print("creating %s" % outfile_name)
            plt.xlim(-1,n_val1)
            plt.xlabel(param_1,fontsize=self.text_size)
            plt.ylabel("Cost",fontsize=self.text_size)
            #lgd = plt.legend(loc=0,prop={'size':self.text_size},mode="expand")
            lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), prop={'size':self.text_size})
            
            #plt.errorbar(x, y, yerr, xerr, fmt, ecolor, elinewidth, capsize, barsabove, lolims, uplims, xlolims, xuplims, errorevery, capthick, hold, data)
            #print(ls_categorical_vals_1)
            plt.gca().set_xticks(np.arange(-1, n_val1 + 2))
            plt.gca().set_xticklabels([' '] + ls_categorical_vals_1 + [' '],rotation=45, ha="right")            
            plt.setp(gca().get_xticklabels(), fontsize=self.text_size)
            plt.setp(gca().get_yticklabels(), fontsize=self.text_size)
            #plt.tight_layout()
            plt.savefig(outfile_name,bbox_extra_artists=(lgd,), bbox_inches='tight')

            # saving output to text files (for further plotting)
            if self.savingOutput:
                outTextFile = outfile_name + '.txt'
                with open(outTextFile, 'wt') as f:
                    f.write('\n'.join(lsOut))

            
    def plot_pairwise_marginal(self, param_1, param_2, lower_bound_1=0, upper_bound_1=1, lower_bound_2=0, upper_bound_2=1, resolution=20):

        dim1, param_name_1 = self._check_param(param_1)
        dim2, param_name_2 = self._check_param(param_2)
                
        grid_1 = np.linspace(lower_bound_1, upper_bound_1, resolution)
        grid_2 = np.linspace(lower_bound_2, upper_bound_2, resolution)
        

        zz = np.zeros([resolution * resolution])
        for i, y_value in enumerate(grid_2):
            for j, x_value in enumerate(grid_1):
                zz[i * resolution + j] = self._fanova._get_marginal_for_value_pair(dim1, dim2, x_value, y_value)[0]

        zz = np.reshape(zz, [resolution, resolution])
        
        
        display_grid_1 = [self._fanova.unormalize_value(param_name_1, value) for value in grid_1]
        display_grid_2 = [self._fanova.unormalize_value(param_name_2, value) for value in grid_2]
        
        
        display_xx, display_yy = np.meshgrid(display_grid_1, display_grid_2)
        
        fig = plt.figure()        
        #ax = fig.gca(projection='3d')
        ax = Axes3D(fig)
        
        surface = ax.plot_surface(display_xx, display_yy, zz, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
        ax.set_xlabel(param_name_1, fontsize=self.text_size)
        ax.set_ylabel(param_name_2, fontsize=self.text_size)
        ax.set_zlabel("Cost", fontsize=self.text_size)
        fig.colorbar(surface, shrink=0.5, aspect=5)
        
        # save output to file
        split = ' '
        if self.savingOutput:
            lsOut = [str(param_name_1 + "_" +param_name_2), split.join([str(x) for x in display_grid]), split.join([str(x) for x in mean]), split.join([str(x) for x in std])]
            outTextFile = directory + '/' + param_name_1 + "_" +param_name_2 + '.png.txt'
            print('saving to ' + outTextFile)
            with open(outTextFile, 'wt') as f:
                f.write('\n'.join(lsOut))        
                
        return plt
    
    
    def plot_marginal(self, param, directory, lower_bound=0, upper_bound=1, is_int=False, resolution=100, log_scale=False, text_size = 10, x_axis_title = True):
        #NGUYEN: add two args: text_size and x_axis_title
        if isinstance(param, int):
            dim = param
            param_name = self._fanova.get_parameter_names()[dim]
        else:
            if param not in self._fanova.param_name2dmin:
                print("Parameter %s not known" % param)
                return
            dim = self._fanova.param_name2dmin[param]
            param_name = param

        if param_name not in self._fanova.get_config_space().get_integer_parameters() and param_name not in self._fanova.get_config_space().get_continuous_parameters():
            print("Parameter %s is not a continuous or integer parameter!" % (param_name)) 
            return 
        grid = np.linspace(lower_bound, upper_bound, resolution)
        display_grid = [self._fanova.unormalize_value(param_name, value) for value in grid]

        mean = np.zeros(resolution)
        std = np.zeros(resolution)
        for i in range(0, resolution):
            (m, s) = self._fanova.get_marginal_for_value(dim, grid[i])
            mean[i] = m
            std[i] = s
        mean = np.asarray(mean)
        std = np.asarray(std)

        lower_curve = mean - std
        upper_curve = mean + std

        if log_scale or (np.diff(display_grid).std() > 0.000001 and param_name in self._fanova.get_config_space().get_continuous_parameters()):
            #HACK for detecting whether it's a log parameter, because the config space doesn't expose this information
            plt.semilogx(display_grid, mean, 'b')
            #print "printing %s semilogx" % param_name
        else:
            plt.plot(display_grid, mean, 'b')
        plt.fill_between(display_grid, upper_curve, lower_curve, facecolor='red', alpha=self.alpha) #NGUYEN: change color from red to yello
        
        plt.setp(gca().get_xticklabels(), fontsize=self.text_size)
        plt.setp(gca().get_yticklabels(), fontsize=self.text_size)
        
        if self.x_axis_title == True:
            plt.xlabel(param_name, fontsize = self.text_size)

        plt.ylabel("Cost", fontsize = self.text_size)

        # save output to file
        split = ' '
        if self.savingOutput:
            lsOut = [param_name, split.join([str(x) for x in display_grid]), split.join([str(x) for x in mean]), split.join([str(x) for x in std])]
            outTextFile = directory + '/' + param_name + '.png.txt'
            print('saving to ' + outTextFile)
            with open(outTextFile, 'wt') as f:
                f.write('\n'.join(lsOut))            

        return plt
    
#     def create_pdf_file(self):
#         latex_doc = self._latex_template
#         with open("fanova_output.tex", "w") as fh:
#             fh.write(latex_doc)        
#             subprocess.call('pdflatex fanova_output.tex')
