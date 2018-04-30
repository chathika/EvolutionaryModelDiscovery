import os
import logging
import sys
import socket
import glob

from subprocess import Popen
from pkg_resources import resource_filename

from pyfanova.fanova_remote import FanovaRemote
#from pyfanova.config_space import ConfigSpace

from ParameterConfigSpace.config_space import ConfigSpace

def check_java_version():
    import re
    from subprocess import STDOUT, check_output
    out = check_output(["java".encode("utf-8"), "-version".encode("utf-8")], stderr=STDOUT).split("\n".encode("utf-8"))
    if len(out) < 1:
        print("Failed checking Java version. Make sure Java version 7 or greater is installed.")
        return False
    m = re.match('java version "\d+.(\d+)..*'.encode("utf-8"), out[0])
    if m is None or len(m.groups()) < 1:
        print("Failed checking Java version. Make sure Java version 7 or greater is installed.")
        return False
    java_version = int(m.group(1))
    if java_version < 7:
        error_msg = "Found Java version %d, but Java version 7 or greater is required." % java_version
        raise RuntimeError(error_msg)
check_java_version()


class Fanova(object):

    def __init__(self, smac_output, num_trees=30,
                 split_min=5,
                 seed=42,
                 improvement_over="NOTHING",
                 quantile_to_compare=0.25,
                 heap_size=1024,
                 fanova_lib_folder=None,
                 fanova_class_folder=None):


        """
            Starts the Fanova from the scenario directory and opens a TCP connection to communicate with Java
            
            Arguments:
              smac_output (str): Path to the state_run directory created by SMAC
              num_trees (int): Number of trees to create the Random Forest
              split_min (int): Minimum number of points to create a new split in the Random Forest
              heap_size (int): Head size in MB for Java
              improvement_over [DEFAULT, QUANTILE, NOTHING]: Compute improvements with respect to (this setting)
              quantile_to_compare (float): Quantile to compare to (if using QUANTILE --improvements-over)
        """
        
        self._remote = FanovaRemote()

        self.check_output_dir(smac_output)

        if fanova_lib_folder is None:
            self._fanova_lib_folder = resource_filename("pyfanova", 'fanova')
        else:
            self._fanova_lib_folder = fanova_lib_folder
        self._fanova_class_folder = fanova_class_folder
        self._num_trees = num_trees
        self._split_min = split_min
        self._seed = seed
        self._smac_output = smac_output
        self._heap_size = "-Xmx" + str(heap_size) + "m"
        self._improvement_over = improvement_over
        self._quantile_to_compare = quantile_to_compare

        self._start_fanova()
        logging.debug("Now connecting to fanova...")
        if self._start_connection():
            if len(glob.glob(os.path.join(smac_output,"*.pcs"))) == 1:
                pcs_file = glob.glob(os.path.join(smac_output,"*.pcs"))[0]
            elif len(glob.glob(os.path.join(smac_output,"params.txt"))) == 1:
                pcs_file = glob.glob(os.path.join(smac_output,"params.txt"))[0]
            elif len(glob.glob(os.path.join(smac_output,"param-file.txt"))) == 1:
                pcs_file = glob.glob(os.path.join(smac_output,"param-file.txt"))[0]
            else:
                print "Error: Couldn't find a parameter configuration space file. Make sure that in the SMAC output directory is a valid file with name *.pcs, params.txt or param-file.txt"
                return
            self._config_space = ConfigSpace(pcs_file)

            param_names = self.get_parameter_names()
            self.param_name2dmin = dict(list(zip(param_names, list(range(len(param_names))))))
        else:
            stdout, stderr = self._process.communicate()
            error_msg = "Failed starting fanova. Did you start it from a SMAC state-run directory?"
            if stdout is not None:
                error_msg += stdout
            if stderr is not None:
                error_msg += stderr
            raise RuntimeError(error_msg)

    def __del__(self):
        if self._remote.connected:
            self._remote.send("die")
            self._remote.disconnect()

    def get_parameter_names(self):

        self._remote.send("get_parameter_names")
        result = self._remote.receive().strip()
        if len(result) > 0:
            names = result.split(';')
        else:
            names = []
            logging.error("No parameters found")
        return names

    def check_output_dir(self, path):
        #if len(glob.glob(os.path.join(p,"*.pcs"))) == 0 or glob.glob(os.path.join(p,"*.pcs"))
        pass 

    def get_marginal(self, param):
        """
            Returns the marginal of param
            
            Arguments:
              param (str): Parameter name
          
            Returns:
              double: marginal
        """
        dim = -1
        if type(param) == int:
            dim = param
        else:
            assert param in self.param_name2dmin, "param %s not known" % param
            dim = self.param_name2dmin[param]
        if dim == -1:
            logging.error("Parameter not found")

        self._remote.send_command(["get_marginal", str(dim)])

        result = self._remote.receive()
        if result == "":
            return float('nan')
        else:
            return float(result)

    def get_pairwise_marginal(self, param1, param2):
        """
            Returns the pairwise marginal between param1 and param2
            
            Arguments:
              param1 (str): Parameter name of param1
              param2 (str): Parameter name of param2
          
            Returns:
              double: marginal
        """
        dim1 = -1
        dim2 = -1
        if type(param1) == int and type(param2) == int:
            dim1 = param1
            dim2 = param2
        else:
            assert param1 in self.param_name2dmin, "param %s not known" % param1
            assert param2 in self.param_name2dmin, "param %s not known" % param2
            dim1 = self.param_name2dmin[param1]
            dim2 = self.param_name2dmin[param2]
        if dim1 == -1 or dim2 == -1:
            logging.error("Parameters not found")

        self._remote.send_command(["get_pairwise_marginal", str(dim1), str(dim2)])
        result = float(self._remote.receive())
        if result == "":
            return float('nan')
        else:
            return float(result)

    def get_marginal_for_value(self, param, value):
        """
            Returns the marginal of param for a specific value
            
            Arguments:
              param (str): Parameter name
              value (double): Value in the interval [0, 1] (Fanova maps it internally to the actual bounds)
          
            Returns:
              double: marginal
        """
        assert value >= 0 and value <= 1
        return self._get_marginal_for_value(param, value)

    def get_categorical_marginal_for_value(self, param, value):
        """
            Returns the categorical marginal for a specific value
            
            Arguments:
              param (str): Parameter name
              value (int): 0-indexed categorical value
          
            Returns:
              double: marginal
        """
        
        size = self._config_space.get_categorical_size(param)
        if(value >= size):
            print("Categorical value %d is out of bounds [%d, %d] for parameter %s" %(value, 0, size, param))
            return
        else:
            return self._get_marginal_for_value(param, value)

    def _get_marginal_for_value(self, param, value):
        
        dim = self._convert_param2dim(param)

        self._remote.send_command(["get_marginal_for_value", str(dim), str(value)])
        result = self._remote.receive().split(';')
        return (float(result[0]), float(result[1]))

    def _get_marginal_for_value_pair(self, param1, param2, value1, value2):
        dim1 = self._convert_param2dim(param1)
        dim2 = self._convert_param2dim(param2)

        self._remote.send_command(["get_marginal_for_value_pair", str(dim1), str(dim2), str(value1), str(value2)])
        result = self._remote.receive().split(';')
        return (float(result[0]), float(result[1]))

    def _convert_param2dim(self, param):
        dim = -1
        if type(param) == int:
            dim = param
        else:
            assert param in self.param_name2dmin, "param %s not known" % param
            dim = self.param_name2dmin[param]
        return dim

    def get_config_space(self):
        """
            Returns the configuration space that was used to build the Random Forest
            
            Returns:
              ConfigSpace
        """
        return self._config_space

    def get_all_pairwise_marginals(self):
        """
            Returns the all pairwise marginal
            
            Returns:
              list: pairwise_marginals
        """
        param_names = self.get_parameter_names()
        pairwise_marginals = []
        for i, param_name1 in enumerate(param_names):
            for j, param_name2 in enumerate(param_names):
                if i <= j:
                    continue
                pairwise_marginal_performance = self.get_pairwise_marginal(i, j)
                pairwise_marginals.append((pairwise_marginal_performance, param_name1, param_name2))
        return pairwise_marginals

    def get_most_important_pairwise_marginals(self, n=10):
        """
            Returns the n most important pairwise marginals
            
            Arguments:
              n (int): The number of pairwise marginals that will be returned
          
            Returns:
              list: pairwise_marginal
        """

        pairwise_marginal_performance = self.get_all_pairwise_marginals()
        pairwise_marginal_performance = sorted(pairwise_marginal_performance, reverse=True)
        important_pairwise_marginals = [(p1, p2) for marginal, p1, p2  in pairwise_marginal_performance[:n]]
        return important_pairwise_marginals

    def print_all_marginals(self, max_num=30, pairwise=True):
        """
            Prints and returns the all marginal
            
            Arguments:
              max_num (int): Maximum number of marginals that will be returned
              pairwise (bool): Considers pairwise marginals or not
          
            Returns:
              list: (marginal, name)
        """

        param_names = self.get_parameter_names()
        num_params = len(param_names)

        main_marginal_performances = [self.get_marginal(i) for i in range(num_params)]
        labelled_performances = []

        for marginal, param_name in zip(main_marginal_performances, param_names):
            labelled_performances.append((marginal, "%.2f%% due to main effect: %s" % (marginal, param_name), param_name))

        print("Sum of fractions for main effects %.2f%%" % (sum(main_marginal_performances)))

        if pairwise:
            pairwise_marginal_performance = self.get_all_pairwise_marginals()
            sum_of_pairwise_marginals = 0
            for pairwise_marginal_performance, param_name1, param_name2 in pairwise_marginal_performance:
                    sum_of_pairwise_marginals += pairwise_marginal_performance
                    label = "%.2f%% due to interaction: %s x %s" % (pairwise_marginal_performance, param_name1, param_name2)
                    labelled_performances.append((pairwise_marginal_performance, label, param_name1 + " x " + param_name2))

            print("Sum of fractions for pairwise interaction effects %.2f%%" % (sum_of_pairwise_marginals))

        sorted_performances = sorted(labelled_performances, reverse=True)
        return_values = []
        if max_num is not None:
            sorted_performances = sorted_performances[:max_num]
        for marginal, label, name in sorted_performances:
            print(label)
            return_values.append((marginal, name))
        return return_values

    def _start_fanova(self):
        cmds = ["java",
            self._heap_size,
            "-cp",
            ":".join(self._fanova_classpath()),
            "net.aeatk.fanova.FAnovaExecutor",
            "--restoreScenario", self._smac_output,
            "--seed", str(self._seed),
            "--rf-num-trees", str(self._num_trees),
            "--split-min", str(self._split_min),
            "--ipc-port", str(self._remote.port),
            "--improvements-over", self._improvement_over,
            "--quantile-to-compare", str(self._quantile_to_compare)
            ]
        #TODO: check that fanova was started successfully and wasn't killed
        with open(os.devnull, "w") as fnull:
            logging.debug(" ".join(cmds))
            if logging.getLogger().level <= logging.DEBUG:
                self._process = Popen(cmds, stdout=sys.stdout, stderr=sys.stdout)
            else:   
                self._process = Popen(cmds, stdout=fnull, stderr=sys.stdout)#stdout=fnull, stderr=fnull)

    def _start_connection(self):
        logging.debug("starting connection...")
        while self._process.poll() is None:
            #while the process is still running we keep on trying to accept the connection
            TIMEOUT = 5
            try:
                self._remote.connect(TIMEOUT)
                logging.debug("connected")
                return True
            except socket.timeout:
                logging.debug("timeout")
                pass
        logging.debug("failed starting fanova")
        #the process terminated without ever instantiating a connection...something went wrong
        return False

    def _fanova_classpath(self):
        classpath = [fname for fname in os.listdir(self._fanova_lib_folder) if fname.endswith(".jar")]
        classpath = [os.path.join(self._fanova_lib_folder, fname) for fname in classpath]
        classpath = [os.path.abspath(fname) for fname in classpath]
        if self._fanova_class_folder is not None:
            classpath.append(os.path.abspath(self._fanova_class_folder))
        logging.debug(classpath)
        return classpath
    
    def unormalize_value(self, parameter, value):
        assert value <= 1 and value >= 0

        self._remote.send_command(["unormalize_value", str(parameter), str(value)])
        value = self._remote.receive()
        if value != "\n":

            return float(value)
        else:
            logging.error("Parameter not found")
            raise ValueError("Parameter not found")
