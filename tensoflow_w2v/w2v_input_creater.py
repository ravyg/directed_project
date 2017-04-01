# -*- coding: utf-8 -*-
import json
import re
import os
import nltk
import csv

# with open("stopwords.txt") as f:
#     stop_words_lst = f.read().splitlines()
# from stop_words import get_stop_words
# stop_words = get_stop_words('english')

from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')

all_known_effects_file = open("se_indi_chv.csv", 'r')
all_key_effects = csv.reader(all_known_effects_file, delimiter=',')

all_effects = []
for row in all_key_effects:
  all_effects.append(row[1])
all_known_effects_file.close()

rootDir = "/media/cit/97711ee6-6425-4985-9701-1cdaa0e358fd/nih/data/s3"
#rootDir = "input_sample"
#bsons = []
total_tweet_count = 0
url_tweet_count = 0
no_url_tweet_count = 0
useful_tweet = 0
discarded = 0

for dir_, _, files in os.walk(rootDir):
    print "dir: " + str(dir_)
    for fileName in files:
        cleaned_tweets = ""
        if fileName.endswith('.json'): 
            relDir = os.path.relpath(dir_, rootDir)
            relFile = os.path.join(rootDir, relDir, fileName)
            # bsons.append(relFile)
            # print "reading file: " + relFile
            bson_file = open(relFile,'r')
            bson_list = bson_file.readlines()
            useful_tweets_per_file = 0
            raw_tweets_list = {}
            for line in bson_list:
                try:
                    tweet = json.loads(line)
                    total_tweet_count = total_tweet_count + 1
                    if  tweet.get('lang') == 'en' and 'text' in tweet.keys() and not tweet['text'].startswith('RT'):
                        # print(json.dumps(tweet, indent=2))
                        #exit()
                        raw_tweet_text = tweet.get('text').encode('utf-8')
                        raw_tweet_id = tweet.get('id')
                        
                        # remove this.
                        # tweet_text = raw_tweet_text.replace('\n', '')
                        # cleaned_tweets = cleaned_tweets + "\n" + tweet_text
                        # print str(total_tweet_count)


                        # discard tweets with URL.
                        #urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_tweet_text)

                        # https = re.findall(r'^https?:\/\/.*[\r\n]*', raw_tweet_text, flags=re.MULTILINE)
                        # http = re.findall(r"http\S+", raw_tweet_text)
                        # text = re.sub(r'^https?:\/\/.*[\r\n]*', '', raw_tweet_text, flags=re.MULTILINE)
                        
                        if "http" not in raw_tweet_text or "https" not in str(raw_tweet_text):
                            # print raw_tweet_text
                        #     exit()

                        # if not https or http:

                            # Strip User mentions.
                            tweet_text = raw_tweet_text.lower()
                            tweet_text = tweet_text.replace('\'', '')
                            tweet_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet_text).split())

                            # tweet_text = ' '.join([word for word in tweet_text.split() if word not in stopwords])
                            no_url_tweet_count = no_url_tweet_count + 1


                            # list_item = str(raw_tweet_id) + '\t' + str(raw_tweet_text)
                            # raw_tweets_list[raw_tweet_id] = raw_tweet_text
                           
                            
                            tweet_with_effect = 0
                            if len(tweet_text.split()) > 2:
                                # tweet_text = [w for w in tweet_text.split() if len(w) >= 2]
                                tokens = tweet_text.split()
                                for word in tokens:
                                    if tweet_with_effect == 0:
                                        if word in all_effects:
                                            tweet_with_effect == 1
                                            # Strip stopwords.
                                            tweet_text = re.sub(r'(.)\1\1+', r'\1\1', tweet_text)
                                            # tweet_text = [w for w in tweet_text.split() if len(w) >= 2]
                                            # tweet_text_str = " ".join(tweet_text)
                                            useful_tweet = useful_tweet + 1
                                            useful_tweets_per_file = useful_tweets_per_file + 1
                                            # cleaned_tweets = cleaned_tweets + " " + tweet_text_str
                                            cleaned_tweets = cleaned_tweets + " " + tweet_text


                                            list_item = str(raw_tweet_id) + '\t' + str(raw_tweet_text)
                                            raw_tweet_text = raw_tweet_text.replace('[ ]+', ' ')
                                            raw_tweets_list[raw_tweet_id] = tweet_text
                        else:
                            url_tweet_count = url_tweet_count + 1

                except:
                    discarded = discarded + 1
                    continue
            bson_file.close()

            #print raw_tweets_list

            # Write ID, texts to file:
            with open("cleaned_data/dec7_16_noURL_tweets.csv", "a") as csv_file:
                wr = csv.writer(csv_file)
                for k, v in raw_tweets_list.items():
                    wr.writerow([k,v])
            # print "writing files records"
            text_file = open("cleaned_data/dec7_16_noURL_tweets.txt", "a")
            text_file.write(cleaned_tweets)
            text_file.close()
            print "Total tweets : " + str(len(bson_list)) + ". Useful tweets in file :" + str(useful_tweets_per_file)
print "Total tweets: " + str(total_tweet_count)
print "discarded tweets count: " + str(url_tweet_count)
print "Tweets without URLS: " + str(no_url_tweet_count)
print "Tweets Processed: " + str(useful_tweet)
print "Tweets discarded: " + str(discarded)

