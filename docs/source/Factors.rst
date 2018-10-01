.. _Factors:

Factors
=======

EvolutionaryModelDiscovery works by combining and re-combining Factors (implmeneted as NetLogo procedures), automatically generating NetLogo models for each combinations, and evaluating them on a modeler-defined objective function. 

Factors are strongly types, i.e. the return type and parameter types must be specified. Only Factors that have a return type equal to a parameter type of another Factor may connect to the second Factor as a child Factor.

**IMPORTANT**: Please, ensure that there is at least one Factor with a matching return type for each parameter type in the entire set of annotated Factors. If there are Factors with parameter types for which there are no Factors with matching return types then an error will be thrown upon initialization.

Tagging Factors
^^^^^^^^^^^^^^^
In NetLogo, an EvolutionaryModelDiscovery factor is essentially a procedure.
You can define EvolutionaryModelDiscovery ready factors by annotations in comments above your reporter.

For a full list of annotations used in EvolutionaryModelDiscovery please refer :ref:`Annotations`.

The typical Factor specification on your model should look as follows

.. code-block:: netlogo

   ;@EMD @factor @return-type=*<return-type>* @parameter-type=*<param1-type>* ... @parameter-type=*<paramN-type>*
   to-report exampleFunction [param1 ... paramN]
   ...
   report *something*
   end

   
Automatically Defined Functions
-------------------------------
To specify an ADF, the @ADF annotation can be used. This is especially useful if a single agent behavior must be represented as the result of one or more encapsulating functions, which must themselves be evolved and evaluated through the genetic program.

.. code-block:: netlogo

   ;@EMD @factor @ADF=*<ADF-name>* @return-type=*<return-type>* @parameter-type=*<param1-type>* ... @parameter-type=*<paramN-type>*
   to-report exampleFunction [param1 ... paramN]
   ...
   report *something*
   end

In the following example, the ``exampleFunction`` is annotated as part of an ADF *emotions*:

.. code-block:: netlogo

   ;@EMD @factor @ADF=emotionalProcess @return-type=polarity-score @parameter-type=neighborhood
   to-report exampleFunction [neighbors]
      ...
   end

