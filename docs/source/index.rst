.. EvolutionaryModelDiscovery documentation master file, created by
   sphinx-quickstart on Wed Sep 26 11:26:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the EvolutionaryModelDiscovery Documentation
=======================================================
Automated agent rule generation and importance evaluation for agent-based models with Genetic Programming and fANOVA.

EvolutionaryModelDiscovery is a framework through which Factors affecting human decision making maybe be assessed on their importance towards the production of a social outcome.

The first phase of EvolutionaryModelDiscovery is evolving combinations of Factors to generate mechanisms for a behavior rule of interest in an ABM. For this, EvolutionaryModelDiscovery performs genetic programming on the supplied ABM, automatically generating and testing versions of the ABM with hypothetical combinations of these Factors. 

Articles: 

- `Gunaratne, C., & Garibay, I. (2017, July).`_ Alternate social theory discovery using genetic programming: towards better understanding the artificial anasazi. In Proceedings of the Genetic and Evolutionary Computation Conference (pp. 115-122). ACM.
- `Gunaratne, C., & Garibay, I. (2018).`_ Evolutionary Model Discovery of Factors for Farm Selection by the Artificial Anasazi. arXiv preprint arXiv:1802.00435.`_

.. _Gunaratne, C., & Garibay, I. (2017, July).: https://dl.acm.org/citation.cfm?id=3071332

.. _Gunaratne, C., & Garibay, I. (2018).: https://arxiv.org/pdf/1802.00435.pdf

Contents
^^^^^^^^

.. toctree::
   :maxdepth: 2
   
   Getting Started
   Factors
   Reference
   License

Requirements
============
EvolutionaryModelDiscovery has the following requirements:

- `Python`_ 2.7 or 3.6  
- `NetLogo`_ 6 or higher
- `JDK`_ 1.8 (Make sure to set the path to the jdk)

.. _Python: https://www.python.org/downloads/release/python-370/
.. _NetLogo: https://ccl.northwestern.edu/netlogo/download.shtml
.. _JDK: https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

EvolutionaryModelDiscovery has several other Python package dependencies that are resolved upon installation.

Installation
============

You can install EvolutionaryModelDiscovery for NetLogo with ``pip``::

   pip install evolutionarymodeldiscovery

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
