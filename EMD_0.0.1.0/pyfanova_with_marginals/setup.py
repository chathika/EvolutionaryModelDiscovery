from setuptools import setup, find_packages

"""
    for the long description, convert:
        https://coderwall.com/p/qawuyq
    or manually here:
        http://johnmacfarlane.net/pandoc/try/
"""

def check_java_version():
    import re
    from subprocess import STDOUT, check_output
    out = check_output(["java".encode("utf-8"), "-version".encode("utf-8")], stderr=STDOUT).split("\n".encode("utf-8"))
    if len(out) < 1:
        print("failed checking Java version. Make sure Java version 7 or greater is installed.")
        return False
    m = re.match('java version "\d+.(\d+)..*'.encode("utf-8"), out[0])
    if m is None or len(m.groups()) < 1:
        print("failed checking Java version. Make sure Java version 7 or greater is installed.")
        return False
    java_version = int(m.group(1))
    if java_version < 7:
        error_msg = "Found Java version %d, but Java version 7 or greater is required." % java_version
 
        raise RuntimeError(error_msg)

def check_java_exists():
    from subprocess import call
    import os
    try:
        devnull = open(os.devnull, 'w')
        call("java", stdout=devnull, stderr=devnull)
    except:
        error_msg = """
        Java not found!

        Fanova needs java in order to work. You can download java from:
        http://java.com/getjava
        """
        raise RuntimeError(error_msg)

check_java_exists()
check_java_version()

setup(
    name = "pyfanova",
    version = "1.0",
    packages = find_packages(),
    install_requires = [
                        'numpy',
                        'docutils>=0.3',
                        'setuptools',
                        'matplotlib>=1.4.2',
                        'ParameterConfigSpace'],

    author = "Tobias Domhan, Aaron Klein (python wrapper). Frank Hutter (FANOVA)",
    author_email = "kleinaa@cs.uni-freiburg.de",
    description = "Functional ANOVA: an implementation of the ICML 2014 paper 'An Efficient Approach for Assessing Hyperparameter Importance' by Frank Hutter, Holger Hoos and Kevin Leyton-Brown.",
    include_package_data = True,
    keywords = "hyperparameter parameter optimization bayesian smac global variance analysis",
    license = "FANOVA is free for academic & non-commercial usage. Please contact Frank Hutter(fh@informatik.uni-freiburg.de) to discuss obtaining a license for commercial purposes.",
    url = "http://automl.org/fanova"
)
