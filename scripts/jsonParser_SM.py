import json
import sys


def fileReader():
    nameTomq = {}
    nameTosc = {}
    nameTosecs = {}
    for line in sys.stdin:
        line = line.rstrip()
        if not line: continue
        jsonObject = json.loads(line)
        if jsonObject.get("is_secondary"):
            name = jsonObject["name"]
            score = jsonObject["score"]
            nameTosecs[name] = score
        else:
            name = jsonObject["name"]
            if jsonObject.get("mapping_quality"):
                mq = jsonObject["mapping_quality"]
                nameTomq[name] = mq
            else:
                mq = 0
                nameTomq[name] = mq
            if jsonObject.get("score"):
                score = jsonObject["score"]
                nameTosc[name] = score
            else:
                score = 0
                nameTosc[name] = score

    for name in nameTosc.keys():
        print(str(name) + "\t", end='')
        print(str(nameTomq[name]) + "\t", end='') if name in nameTomq.keys() else print(
            "0" + "\t", end='')
        print(str(nameTosc[name]) + "\t", end='') if name in nameTosc.keys() else print(
            "0" + "\t", end='')
        print(str(nameTosecs[name]) + "\t", end='') if name in nameTosecs.keys() else print(
            "0" + "\t", end='')
        print("")
fileReader()
