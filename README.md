# Renault-Zoe-API-Prtg
Renault Zoe API, modified for a PRTG Custom Python Sensor

Based on https://github.com/edent/Renault-Zoe-API

Genereal Instructions:
1. cd C:\Program Files (x86)\PRTG Network Monitor\Python34
2. download https://bootstrap.pypa.io/get-pip.py There.
3. (WITH ADMIN!) python.exe get-pip.py
4. cd C:\Program Files (x86)\PRTG Network Monitor\Python34\Scripts
5. (WITH ADMIN!) pip install requests
6. copy files from this project to C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python
7. change credentials.json with relevant cred's.
8. create a new custom python sensor, and select zoe-console.py as the script. i suggest a frequency of 5 minutes.

If something isn't working, try running 
"C:\Program Files (x86)\PRTG Network Monitor\Python34\python.exe" "C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python\zoe-console.py" 
in a command shell and open an issue with the results.
