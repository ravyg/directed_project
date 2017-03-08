# -*- coding: utf-8 -*-
import json
import re
import os
import csv
rootDir = "data/"

join_words_list = ['st johns wort', 'stjohns wort', 'stjohn s wort', 'st john s wort', 'stjohn swort', 'stjohnswort', 'st johnswort', 'john s wort', 'johnswort', 'johnwort', 'john swort', 'johns wort' ]
cleaned_tweets = ""
for line in open(rootDir+'37k_yb_sup','r').readlines():
        # Strip URLS.
        tweet_text = re.sub(r"https\S+", "", line)
        tweet_text = re.sub(r"http\S+", "", tweet_text)
        # Strip User mentions.
        tweet_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)","",tweet_text).split())
        # Strip all special chars.
        #tweet_text = re.sub('[^A-Za-z0-9]+', ' ', tweet_text)
        tweet_text = re.sub(r'(.)\1\1+', r'\1\1', tweet_text)
        tweet_text = tweet_text.lower()
        big_regex = re.compile('|'.join(map(re.escape, join_words_list)))
        tweet_text = big_regex.sub("stjohnswort", tweet_text)
        tweet_text = [w for w in tweet_text.split() if len(w) >= 2]
        tweet_text_str = " ".join(tweet_text)
        cleaned_tweets = cleaned_tweets + " " + tweet_text_str
        
text_file = open(rootDir+"37k_yb_sup_cleaned.txt", "a")
text_file.write(cleaned_tweets)
text_file.close()

