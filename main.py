#Welcome to Rezi!
#    ____             _ 
#   / __ \___  ____  (_)
#  / /_/ / _ \/_  / / / 
# / _, _/  __/ / /_/ /  
#/_/ |_|\___/ /___/_/   
#Rezi was written in Python 3.9.6 on Sublime Text.
#Please visit the github at https://github.com/Wamy-Dev/ReziWebsite
import requests                                       
import sys
from datetime import datetime
sys.path.append('./components')
#
now=datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Time started: {current_time}.")
#
import grabber