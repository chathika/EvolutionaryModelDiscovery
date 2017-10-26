ECHO
ECHO Starting Evolutionary Model Discovery. Authored by Chathika Gunaratne contact: chathika@knights.ucf.edu 
REM Change directory to ecj\ecj
cd ecj\ecj
REM Run ECJ on EMD Spec application. Also provide netlogo libraries path
java -cp .;"..\..\Anasazi\NetLogo 6.0.1\app\netlogo-6.0.1.jar";..\..\EMD_Spec\ ec.Evolve -file ..\..\EMD_Spec\EMD_ArtificialAnasazi.params
REM Change directory back
cd ..\..