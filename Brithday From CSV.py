import csv
import urllib.request
import wikipedia
import wptools
from tqdm import tqdm
import io
import pandas as pd

retVal = {}
with open("new_celebs.csv", mode='r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    line_count = 0
    for row in reader:
        # print(row)
        if line_count != 0:
            retVal[row[0]] = row[1]
        else:
            line_count = line_count+1