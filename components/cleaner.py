import json
#loads json file
try:
  json_file = open("./components/output.json")
  strings = json.load(json_file)
except:
  print('Json file to be cleaned not found.')
#Single version, used best on a single key or target
#target_key = "switch-1-105518"
#target_string = "https://nsw2u.xyz/aaa-clock-switch-nsp"
#while True:#user input version
#    target_key = s if (s:=input('Enter Key (leave blank to repeat previous):')) else target_string
#    if target_key == 'q':
#        print('Stopping and Saving'):
#        break
#    target_string = s if (s:=input('Enter String (leave blank to repeat previous):')) else target_string
#    strings[target_key] = [s for s in strings[target_key] if s != target_string]

#Automated version, used on multiple keys and targets
try: 
  targets = {'marked':['https://masquerade.site#a-z-listing-1'],'marked':['https://nsw2u.xyz/#a-z-listing-2'],'marked':['https://madloader.com/request/'],'marked':['https://nxbrew.com/#a-z-listing-1'],'marked':['https://archive.org/download/mame-merged/mame-merged/../']}#add pairs here, or structure differently up to you format: 'key2':['target1','target2']
  for target_key,target_strings in targets.items():
      strings[target_key] = [s for s in strings[target_key] if s not in target_strings]
  with open("./components/outputcleaned.json", "w", encoding="utf-8") as file:#dumps to new json file to be used in totable.py
    file.write(
    json.dumps(strings)
    )
except:
  print('Key(s) marked for cleaning nonexistent, completed.')
import forsearch
