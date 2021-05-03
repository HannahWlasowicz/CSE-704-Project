import csv
import twitter
import json
from langdetect import detect
from textblob import TextBlob
import re
from collections import defaultdict

def normalize_word(word):
    
    word = re.sub(r'[^\w\s]', '', word)
    word = word.replace('\n', '')
    word = word.lower()
    return word 

def filter_word(word):
    if len(word)==0:
        return False
    if word[0]=='@' or word[0] == '.':
        return False
    if word.startswith('http'):
        return False
    return True



with open('credentials.txt') as file:
    file_json = json.loads(file.read())

twitter_api = twitter.Api(consumer_key=file_json["API_KEY"],
                  consumer_secret=file_json["API_SECRET_KEY"],
                  access_token_key=file_json["ACCESS_TOKEN"],
                  access_token_secret=file_json["ACCESS_TOKEN_SECRET"])


age_dict = dict()
with open("csv/wiki_data.csv", mode='r') as wiki_csv:
    reader = csv.reader(wiki_csv, delimiter=',')
    for row in reader:
        age = row[2]
        handle = row[3]
        age_dict[handle] = age

word_dict = dict()
with open("csv/wiki_data.csv", mode='r',) as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        handle = row[3]
        word_dict[handle] = defaultdict(int)
        try:
            tweets = twitter_api.GetUserTimeline(screen_name=handle, count=200)
            parsed_lang = " ".join(tweets[0].text.split(" "))
            detected_language = TextBlob(parsed_lang).detect_language()
            if detected_language=="en" and handle in age_dict:
                for tweet in tweets:
                    words = tweet.text.split(' ')
                    for word in words:
                        if filter_word(word):
                            word_dict[handle][normalize_word(word)]+=1
            else:
                print("not the right language: " + detected_language + " " + handle + ", "+ parsed_lang)
        except:
            print(handle)
json = json.dumps(word_dict)
print(len(word_dict))
f = open("word_dict.json","w")
f.write(json)
f.close()




