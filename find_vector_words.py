import json
import operator
from collections import defaultdict
word_dict = dict()

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = dict1[key]+dict2[key]
   return dict3


with open("word_dict.json", mode="r") as jsonfile:
    json_data = json.loads(jsonfile.read())
    for item in json_data:
        current_dict = json_data[item]
        word_dict = mergeDict(word_dict, current_dict)


filtered_dict = {k:v for (k,v) in word_dict.items() if v>10}


with open('csv/words_in_vec.csv', mode="w") as file:
    for item in filtered_dict:
        if item!="":
            file.write(item + ", " + str(filtered_dict[item]) + "\n")



        