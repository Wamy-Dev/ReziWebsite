import json
import random
import string
from urllib.parse import unquote
def listToString(s): 
    # initialize an empty string
    str1 = "" 
    count=0
    # traverse in the string  
    for ele in s: 
        str1 += ele
        count+=1
        if count==len(s):
          continue
        else:
          str1+=" "  
    # return string  
    return str1 
input_file =  './components/outputcleaned.json'  # input file 
output_file = './components/outputsearchready.json'
# Opening JSON file
f = open(input_file)
N=10  # ID length 
count= 0 
dic= {}  # to store overal output
data = json.load(f) 
for k in data.keys():
  key = k
  lst= []
  count+=1
  for sub_k in data[k]: #  access each entry 
    ID= ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N)) # generating IDs of N length
    j = sub_k.split("/")[-1]
    if j=='':
      j= sub_k.split("/")[-2]
    name=None
    if "-" in j:
      name = j.split("-")
    else:
      name= j.split("_")
    name = [nam.title() for nam in name ]
    name = listToString(name)
    name = unquote(name)
    # print(sub_k.replace("https://",""), j, name)
    lst.append({"id":ID, "basename":name.replace("%",""),"link":sub_k.replace("https://","")})
  dic[key] = lst
  # comment next two lines, if you want output for all objects. This 'IF' is just for three objects to check output
  #if count==3:
  #  break
with open(output_file, "w") as outfile:
    json.dump(dic, outfile)
json_file = open("./components/outputsearchready.json")
file = json.load(json_file)
data = file.pop('marked')
with open("./components/outputsearchready.json", "w", encoding="utf-8") as file:#dumps to new json file to be used in totable.py
  file.write(
  json.dumps(data)
  )
import sendtosearch
