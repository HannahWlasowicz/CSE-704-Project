import csv 
with open('training_data.csv', mode="r") as training_data:
    with open('new_training_data.csv', mode="w") as new_training_datas:
        reader = csv.reader(training_data)
        writer = csv.writer(new_training_datas)
        for i, row in enumerate(reader):
            if i>0:
                new_row = map(lambda x: int(x) , row[1:-2])
                if sum(new_row) > 0:
                    writer.writerow(row)
            else:
                writer.writerow(row)
