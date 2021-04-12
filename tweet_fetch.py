import csv
import twitter
import json
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

word_dict = dict()
with open("top-1000-celebs.csv", mode='r',) as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        handle = row[0]
        word_dict[handle] = defaultdict(int)
        try:
            tweets = twitter_api.GetUserTimeline(screen_name=handle, count=200)
            for tweet in tweets:
                words = tweet.text.split(' ')
                for word in words:
                    if filter_word(word):
                        word_dict[handle][normalize_word(word)]+=1
        except:
            print(handle)
json = json.dumps(word_dict)
f = open("word_dict.json","w")
f.write(json)
f.close()




