javac -d bin/server -cp "C:/Users/ch328575/AppData/Local/Continuum/Anaconda2/share/py4j/py4j0.10.6.jar;C:/Program Files/NetLogo 6.0.2/app/netlogo-6.0.2.jar;." src/server/bsearch/space/*.java src/server/bsearch/nlogolink/*.java src/server/emd/server/*.java
cp src/server/Manifest.txt bin/server
cd bin/server
jar cvfm NetLogoControllerServer.jar Manifest.txt emd/server/NetLogoControllerServer.class bsearch emd
cd ../..

