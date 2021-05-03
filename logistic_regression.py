import csv
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn.preprocessing as preprocessing
word_set = set()
with open("csv/words_in_vec.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        word_set.add(row[0])
word_set = list(word_set)


with open("csv/wiki_data.csv", mode='r') as wiki_csv:
    age_dict = dict()
    reader = csv.reader(wiki_csv, delimiter=',')
    for row in reader:
        age = row[2]
        handle = row[3]
        age_dict[handle] = age


with open('csv/training_data.csv', mode="w") as csvfile:
    with open("word_dict.json", mode="r") as jsonfile:
        csv_writer = csv.writer(csvfile)
        celebs_word_dict = json.loads(jsonfile.read())
        
        csv_writer.writerow(["handle"] + word_set + ["age"])
        target = np.zeros(len(celebs_word_dict))
        for j, handle in enumerate(celebs_word_dict):
            data = [0]*len(word_set)
            celeb_dict = celebs_word_dict[handle]
            for i, word in enumerate(word_set):
                if word in celeb_dict:
                    data[i] = celeb_dict[word]
            age = age_dict[handle] if handle in age_dict else -1
            if (age !=-1 and age!="") and sum(data)>0:
                csv_writer.writerow([handle]+ data + [age])
            target[j] = int(age)

data = pd.read_csv('training_data.csv')

x = data.drop(data.columns[[0,1, -1]], axis=1)
y = data.iloc[:,-1:]


        
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

minmax = preprocessing.MinMaxScaler()
minmax.fit(x_train)
x_train = minmax.transform(x_train)
x_test = minmax.transform(x_test)
regressor = LinearRegression()
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)
from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

y_pred = pd.DataFrame(y_pred)
y_test = pd.DataFrame(y_test)
y_test.reset_index(drop=True, inplace=True)


df = pd.DataFrame({'actual': y_test.iloc[:, 0], 'pred': y_pred.iloc[:, 0]})

print(df.head)
