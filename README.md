# S3Camera
LED iBOND Library to work with a camera object and update images from client to a web storage (S3 AWS) on regular interval
## Requiremnets

the following are neded for the functionality of the barnch
1. aws login credentials
2. aws bucket defined by a manager commissioned for particular project.
3. Darknet dependencies exist for on board detection

## Stream beta version
The branch capabilities so far is to 
1. Capture images from a connected webcam and upload on a local predefined aws project bucket
2. Perform detection on image present in cloud storage on configured Darknet detector 
