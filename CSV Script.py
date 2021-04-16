import csv
import urllib.request
import wikipedia
import wptools
from tqdm import tqdm
import io
import pandas as pd

# link = "https://gist.githubusercontent.com/mbejda/9c3353780270e7298763/raw/1bfc4810db4240d85947e6aef85fcae71f475493/Top-1000-Celebrity-Twitter-Accounts.csv"
# file = urllib.request.urlopen(link)
retVal = {}
# for line in file:
#     decoded_line = line.decode("utf-8")
#     arr = decoded_line.split(",")
#     retVal[arr[0]] = arr[2]


#Read from CSV with utf8 encoding
with open("csv/new_celebs.csv", mode='r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    line_count = 0
    for row in reader:
        # print(row)
        if line_count != 0:
            retVal[row[0]] = row[1]
        else:
            line_count = line_count+1

# print(retVal["khloekardashian"])

#Write to CSV with utf8 encoding
# with open('test.csv', mode='w', encoding="utf-8") as employee_file:
#     writer = csv.writer(employee_file, delimiter=',')
#     for key in retVal:
#         if key:
#             writer.writerow([key, retVal[key]])
# print("Done")
names = []
for key in retVal:
    names.append(retVal[key])

wiki_data = []
fails = []

name_to_handle = {}
for handle in retVal:
    name_to_handle[retVal[handle]] = handle



# try:
#     wiki_data.append((names[0], wikipedia.page(names[0].strip())))
# except wikipedia.DisambiguationError:
#     # print('cant disambiguate', line)
#     fails.append(line)
# except wikipedia.PageError:
#     # print('cant find', line)
#     fails.append(line)

# infobox_data = []
# name = wiki_data[0][0]
# wiki_pg = wiki_data[0][1]
# # for name, wiki_pg in tqdm(wiki_data):
# print(wiki_data[0][1].title)
# try:
#     parse = wptools.page(wiki_pg.title).get_parse()
#     infobox_data.append((name, parse))
# except LookupError:
#     print("hi")
    

# # print(infobox_data[0])

# parsed_infobox_data = []
# infobox_fields = ['birth_date', 'name']
# for name, u in infobox_data:
#     dat = {"name" : name.strip()}
#     if 'infobox' in u.data and u.data['infobox']:
#         print(u.data['infobox'])
#         print(u.data['infobox'].keys())
#         for x in infobox_fields:
#             print(u.data['infobox'].get(x, ''))
#             dat[x] = u.data['infobox'].get(x, '')
#     else:
#         for x in infobox_fields:
#             dat[x] = ''
#             print("Rip")
#     parsed_infobox_data.append(dat)

# Change this to names in the csv file
to_wikify = [x for x in names]
for line in tqdm(names):
    try:
        wiki_data.append((line, wikipedia.page(line.strip())))
    except wikipedia.DisambiguationError as e:
        # print('cant disambiguate', line)
        # print(e.options)
        fails.append((line, name_to_handle[line]))
    except wikipedia.PageError:
        # print('cant find', line)
        fails.append((line, name_to_handle[line]))


infobox_data = []
for name, wiki_pg in tqdm(wiki_data):
    # print(wiki_pg.title)
    try:
        parse = wptools.page(wiki_pg.title).get_parse()
        infobox_data.append((name, parse))
    except LookupError:
        continue
    except UnicodeEncodeError:
        continue

# print(infobox_data[0])

parsed_infobox_data = []
infobox_fields = ['birth_date', 'name']
for name, u in infobox_data:
    
    dat = {"name" : name}
    if 'infobox' in u.data and u.data['infobox']:
        for x in infobox_fields:
            dat[x] = u.data['infobox'].get(x, '')
    else:
        for x in infobox_fields:
            dat[x] = ''
    dat["twitter"] = name_to_handle[name]
    parsed_infobox_data.append(dat)


infoboxes = pd.DataFrame(parsed_infobox_data)
infoboxes.to_csv("csv/wiki_data.csv",encoding="utf8")
failed = pd.DataFrame(fails)
failed.to_csv("csv/failed.csv", encoding="utf8")