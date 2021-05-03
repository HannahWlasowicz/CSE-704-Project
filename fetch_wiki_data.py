import csv
import urllib.request
import wikipedia
import wptools
from tqdm import tqdm
import io
from datetime import date
import pandas as pd

def parse_birth_date(birthday):
    birthday = birthday.replace('{', '')
    birthday = birthday.replace('}', '')
    birth_data = birthday.split('|')
    try: 
        if len(birth_data) > 4:
            if len(birth_data[1]) != 4:
                # at end
                birth_year = int(birth_data[4])
                birth_month = int(birth_data[5])
                birth_day =  int(birth_data[6])
            else:
                birth_year = int(birth_data[1])
                birth_month = int(birth_data[2])
                birth_day =  int(birth_data[3])
            today = date.today()
            age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
            return age

        elif len(birth_data) < 4:
            return 0
        else:
            birth_year = int(birth_data[1])
            birth_month = int(birth_data[2])
            birth_day =  int(birth_data[3])
            today = date.today()
            age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
            return age
    except:
        return -1

#Read from CSV with utf8 encoding
names = list()
name_to_handle = dict()
with open("csv/new_celebs.csv", mode='r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        handle = row[0]
        name = row[1]
        names.append(name)
        name_to_handle[name] = handle

wiki_data = []
fails = []

# Change this to names in the csv file
infobox_data = list()
for line in tqdm(names):
    try:
        processed_name = line.strip().lower().title()
        find_page = wikipedia.page(processed_name, auto_suggest=False)
        parse = wptools.page(find_page.title).get_parse()
        infobox_data.append((line, parse))
    except wikipedia.DisambiguationError as e:
        print('cant disambiguate', line)
        print(e.options)
        fails.append((line, name_to_handle[line]))
    except wikipedia.PageError:
        print('cant find', line)
        fails.append((line, name_to_handle[line]))
    except LookupError:
        continue
    except UnicodeEncodeError:
        continue


parsed_infobox_data = []
for name, u in infobox_data:
    dat = {"name" : name}
    if 'infobox' in u.data and u.data['infobox']:
        dat['birth_date'] = parse_birth_date(u.data['infobox'].get('birth_date', ''))
        if dat['birth_date']==0:
            continue
    else:
            dat['birth_date'] = ''
    dat["twitter"] = name_to_handle[name]
    parsed_infobox_data.append(dat)


infoboxes = pd.DataFrame(parsed_infobox_data)
infoboxes.to_csv("csv/wiki_data.csv",encoding="utf8")
failed = pd.DataFrame(fails)
failed.to_csv("csv/failed.csv", encoding="utf8")