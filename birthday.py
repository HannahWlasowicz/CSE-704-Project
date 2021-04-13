import csv
import io
import re
from datetime import date

retVal = []
with open("wiki_data.csv", mode='r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    
    line_count = 0
    for row in reader:
        dat = {}
        # print(row)
        if line_count != 0:
            dat["name"] = row[0]
            dat["bday"] = row[1]
            dat["twitter"] = row[2]
            retVal.append(dat)
        else:
            line_count = line_count+1

for val in retVal:
    birthday = val["bday"]
    birthday = birthday.replace('{', '')
    birthday = birthday.replace('}', '')
    birth_data = birthday.split('|')
    if len(birth_data) > 0:
        if len(birth_data) > 4 or len(birth_data) <4:
            # Parse out stuff
            print(birth_data)
        else:
            print(birth_data)
            birth_year = int(birth_data[1])
            birth_month = int(birth_data[2])
            birth_day =  int(birth_data[3])
            today = date.today()
            age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
            val["bday"] = age


with open('updated_wiki_data.csv', mode='w', encoding="utf-8") as employee_file:
    writer = csv.writer(employee_file, delimiter=',')
    for val in retVal:
        writer.writerow([val["name"],val["bday"], val["twitter"] ])