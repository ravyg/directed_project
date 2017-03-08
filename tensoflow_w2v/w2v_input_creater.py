# -*- coding: utf-8 -*-
import json
import re
import os
import nltk

# with open("stopwords.txt") as f:
#     stop_words_lst = f.read().splitlines()
# from stop_words import get_stop_words
# stop_words = get_stop_words('english')

from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')


rootDir = "/media/cit/97711ee6-6425-4985-9701-1cdaa0e358fd/nih/data/s3"
#bsons = []
#join_words_list = ['st johns wort', 'stjohns wort', 'stjohn s wort', 'st john s wort', 'stjohn swort', 'stjohnswort', 'st johnswort', 'john s wort', 'johnswort', 'johnwort', 'john swort', 'johns wort' ]
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
            for line in bson_list:
                try:
                    tweet = json.loads(line)
                    total_tweet_count = total_tweet_count + 1
                    if  tweet.get('lang') == 'en' and 'text' in tweet.keys() and not tweet['text'].startswith('RT'):
                        #print(json.dumps(tweet, indent=2))
                        #exit()
                        raw_tweet_text = tweet.get('text').encode('utf-8')

                        # remove this.
                        tweet_text = raw_tweet_text.replace('\n', '')
                        cleaned_tweets = cleaned_tweets + "\n" + tweet_text
                        print str(total_tweet_count)


                        # discard tweets with URL.
                        # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_tweet_text)

                        # if not urls:
                        #     # Strip User mentions.
                        #     tweet_text = raw_tweet_text.lower()
                        #     tweet_text = tweet_text.replace('\'', '')
                        #     tweet_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet_text).split())
                        #     tweet_text = ' '.join([word for word in tweet_text.split() if word not in stopwords])
                        #     no_url_tweet_count = no_url_tweet_count + 1
                            
                        #     if len(tweet_text.split()) > 2:
                        #         # Strip stopwords.
                        #         tweet_text = re.sub(r'(.)\1\1+', r'\1\1', tweet_text)
                        #         tweet_text = [w for w in tweet_text.split() if len(w) >= 4]
                        #         tweet_text_str = " ".join(tweet_text)
                        #         useful_tweet = useful_tweet + 1
                        #         useful_tweets_per_file = useful_tweets_per_file + 1
                        #         cleaned_tweets = cleaned_tweets + " " + tweet_text_str
                        # else:
                        #     url_tweet_count = url_tweet_count + 1
                except:
                    discarded = discarded + 1
                    continue
            bson_file.close()
            # print "writing files records"
            text_file = open("cleaned_data/22m_s3_raw_.txt", "a")
            text_file.write(cleaned_tweets)
            text_file.close()
            print "Total tweets : " + str(len(bson_list)) + ". Useful tweets in file :" + str(useful_tweets_per_file)
print "Total tweets: " + str(total_tweet_count)
# print "discarded tweets count: " + str(url_tweet_count)
# print "Tweets without URLS: " + str(no_url_tweet_count)
# print "Tweets Processed: " + str(useful_tweet)
print "Tweets discarded: " + str(discarded)

