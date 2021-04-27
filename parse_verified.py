import json
with open('verified_celebs.csv', mode="w") as writefile:
    with open("TU_verified_2019-05-22.json", mode='r',) as jsonfile:
        count = 0
        for row in jsonfile:
            if count>10:
                break
            row = json.loads(row)
            if row["followers_count"]>100000:
                count+=1
                writefile.write(row["screen_name"]+ ", " + row["name"] + "\n")
