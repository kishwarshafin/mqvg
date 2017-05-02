import argparse
import sys
import os


def convert(compare_file, tab_file):
    mapqualityDictionary = {} #read_name -> (true, mapping_quality)
    for line in open(compare_file):
        line = line.rstrip()
        line = line.replace(',','')
        splitList = line.rstrip().split(' ')
        if len(splitList)<2:
            mapqualityDictionary[splitList[0]] = (0,0)
            continue
        mapqualityDictionary[splitList[0]] = (splitList[1],splitList[2])

    scoreDictionary = {} #read_name -> score
    for line in open(tab_file):
        splitList = line.rstrip().split('\t')
        if len(splitList)<2:
            scoreDictionary[splitList[0]] = 0
            continue
        scoreDictionary[splitList[0]] = splitList[2]

    keys = list(mapqualityDictionary.keys())

    for key in keys:
        print(key+"\t"+str(mapqualityDictionary[key][1])+"\t"+str(scoreDictionary[key])+"\t"+str(mapqualityDictionary[key][0]))


FLAGS = None

def main():
    convert(FLAGS.compare_file, FLAGS.tab_converted_file)



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")
  parser.add_argument(
      "--compare_file",
      type=str,
      default="",
      help="Compare file produced by vg sim. {Read->(mapping quality, match/mistmatch)}"
  )
  parser.add_argument(
      "--tab_converted_file",
      type=str,
      default="",
      help="File converted from gam to tab delimated file. {Read->Score}"
  )
  FLAGS, unparsed = parser.parse_known_args()
  main()