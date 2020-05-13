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
import re
import pkg_resources
import os
import functools
import inspect
import warnings

def netlogo_EMD_line_to_array(netlogo_EMD_line):
    netlogo_EMD_line = netlogo_EMD_line.lower()
    if "@emd" in netlogo_EMD_line:
        return re.sub("[\s;]","",netlogo_EMD_line).split("@")
    else:
        raise Exception("Not an EMD annotated line: {}".format(netlogo_EMD_line))

def get_model_factors_path():
    model_factors_file_path = pkg_resources.resource_filename('EvolutionaryModelDiscovery', 'ModelFactors.py')    
    return model_factors_file_path

def remove_model_factors_file():
    if os.path.exists(get_model_factors_path()):
        os.remove(get_model_factors_path())

def create_model_factors_file():
    if os.path.exists(get_model_factors_path()):
        open(get_model_factors_path(),"w+")

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens."""
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '_', value).lower())
    return value


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

def is_locked(filepath):
    """Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """
    locked = None
    file_object = None
    #if os.path.exists(filepath):
    try:
        #print("Trying to open {0}.".format( filepath))
        buffer_size = 8
        # Opening file in append mode and read the first 8 characters.
        file_object = open(filepath, 'a', buffer_size)
        if file_object:
            #print("{0} is not locked.".format(filepath))
            locked = False
    except IOError as message:
        raise Exception("(unable to open in append mode).{0}.".format(message))
        locked = True
    finally:
        if file_object:
            file_object.close()
            #print("{0} closed.".format(filepath))
    #else:
    #    print("{0} not found.".format(filepath))
    return locked

def wait_for_files(filepaths):
    """Checks if the files are ready.

    For a file to be ready it must exist and can be opened in append
    mode.
    """
    wait_time = 0.05
    for filepath in filepaths:
        # If the file doesn't exist, wait wait_time seconds and try again
        # until it's found.
        #while not os.path.exists(filepath):
        #    print("{0} hasn't arrived. Waiting {1} seconds.".format(filepath, wait_time))
        #    time.sleep(wait_time)
        # If the file exists but locked, wait wait_time seconds and check
        # again until it's no longer locked by another process.
        while is_locked(filepath):
            #print(filepath)
            #print("waiting on file")
            #print("{0} is currently in use. Waiting {1} seconds.".format(filepath, wait_time))
            time.sleep(wait_time)


string_types = (type(b''), type(u''))


def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    if isinstance(reason, string_types):

        # The @deprecated is used with a 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated("please, use another function")
        #    def old_function(x, y):
        #      pass

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Call to deprecated class {name} ({reason})."
            else:
                fmt1 = "Call to deprecated function {name} ({reason})."

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):

        # The @deprecated is used without any 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated
        #    def old_function(x, y):
        #      pass

        func2 = reason

        if inspect.isclass(func2):
            fmt2 = "Call to deprecated class {name}."
        else:
            fmt2 = "Call to deprecated function {name}."

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))