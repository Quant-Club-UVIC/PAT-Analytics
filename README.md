# PAT-Analytics
PAT-Analytics is a python library that allows user to fetch market data, create a portfolio, perform calculations and display portfolio metrics
: risk, sector allocations, implied growth, stress-tests, portfolio optimizations. Is meant to be usable as a stand-alone application.

# Quick Set-Up  
Need to install the necessary dependancies, after cloning the repo in main/ type  
```python3
python3.12 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```  

# Code-Base  
Main source-code is located in pat_analytics/ , the main object *Portfolio* is defined in portfolio.py. If you wish to see how to run our code check out examples/. All of our work-in-progress notebooks and scripts are in work-in-progress/.  

# To Contributors  
If you add dependencies to this project (pandas, requests, etc) you must update the requirements.txt, you can do this by  
```python3
pip3 install pipreqs  
pipreqs --force ./
```
Do this in main/ of course.  
If you have come up with a new model, add your whitepaper for it in documentation/
# Contributors  
Add here later