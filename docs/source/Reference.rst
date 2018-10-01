Reference
=========


.. _Annotations:

Annotations
-----------

EvolutionaryModelDiscovery uses comment annotations when identifying parts of the NetLogo model to be evolved. 

Below is a complete list of annotations used in EvolutionaryModelDiscovery:

+----------------+--------------------------------------+-----------------------------------------------+
|   Annotation   |    Example                           |                                      Meaning  |
+================+======================================+===============================================+
|@EMD            | @factors-file="util/Functions.nls"   |Indicates the start of an EMD specification    |
+----------------+--------------------------------------+-----------------------------------------------+
|@EvolveNextLine | @EvolveNextLine                      |Indicates that the next line as the entry point|
|                |                                      |for evolution of the behavior rule             |
+----------------+--------------------------------------+-----------------------------------------------+
|@factors-file   | @factors-file="util/FactorsFile.nls" |                                               |
+----------------+--------------------------------------+-----------------------------------------------+
|@return-type    | @return-type=patchTypeA              |Factor below returns something of the specified|
+----------------+--------------------------------------+-----------------------------------------------+
|@parameter-type | @parameter-type=emotion              | Factor below takes a parameter of this type   |
+----------------+--------------------------------------+-----------------------------------------------+
|@ADF            | @ADF=emotionalProcess                | ADF to which this factor belongs              |
+----------------+--------------------------------------+-----------------------------------------------+