# SI-507-FinalProject

### files ###
There are three .py files named scrapehello.py, flaskhello.py and readJson.py  
The first file is to scrape relevant data from websites and cache them as .json.
The second file is to run Flask app, and
the third one is to read cached file and pass variables to Flask  


### steps ###
The first step is to run scrapehello.py to fetch data and cache it.  
Then run the flaskhello.py to start a Flask app and take a look at 127.0.0.1/5000  
 

### interatctions ###
When users visit the website, ‘Welcome to the Eastfund website!’ will first appear. 
There is also a link towards the interactive page at the bottom of the welcome page, where some user input options will appear. 
There are four options in total that users can select. 
The first one is to select a specific fund type. 
When the link is clicked, a new page will be directed to, where users can select whether to look at OE funds or ET funds. 
When the form is submitted, relevant funds information will appear on a new webpage. 
The second option is to choose a specific fund. 
When the second link is clicked, a new page with all funds’ options will appear regardless of fund types. 
The third option is to look at a specific fund manager. 
The fourth option is to take a look at all the funds without any preferences. 
At the bottom of each page except the homepage, there are also two links whether to go back to the last webpage or revisit the homepage.  


### requirements ###
import json  
import time  
from bs4 import BeautifulSoup  
import requests  
import re  
from flask import Flask,render_template, request  


### data structure ###
A graph structure is constructed using dictionaries.  
There are two types of nodes in the graph, i.e., funds nodes and managers nodes. 
The funds nodes are also divided into two to distinguish between two different fund types. 
And the vertices are the connections between managers and the funds. 
funds:{type1:{fund_name:{managers}}, type2:{fund_name:{managers}}}
managers:{name:{funds}}  
Recall the data structure we used in the Kevin-Bacon problem.
