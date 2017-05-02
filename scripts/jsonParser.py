import json
import sys


def fileReader():
    for line in sys.stdin:
        line = line.rstrip()
        if not line: continue
        jsonObject = json.loads(line)
        print(jsonObject["name"]+"\t", end='') if jsonObject.get("name")  else print(" "+"\t", end='')
        print(str(jsonObject["mapping_quality"])+"\t", end='') if jsonObject.get("mapping_quality")  else print("0"+"\t", end='')
        print(str(jsonObject["score"])+"\t", end='') if jsonObject.get("score")  else print("0"+"\t", end='')
        print("")



fileReader()
