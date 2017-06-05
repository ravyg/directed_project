###############################################################################################
#
# Script for training good word and phrase vector model using public corpora, version 1.0.
# The training time will be from several hours to about a day.
#
# Downloads about 8 billion words, makes phrases using two runs of word2phrase, trains
# a 500-dimensional vector model and evaluates it on word and phrase analogy tasks.
#
###############################################################################################

# This function will convert text to lowercase and remove special characters
# normalize_text() {
#   awk '{print tolower($0);}' | sed -e "s/’/'/g" -e "s/′/'/g" -e "s/''/ /g" -e "s/'/ ' /g" -e "s/“/\"/g" -e "s/”/\"/g" \
#   -e 's/"/ " /g' -e 's/\./ \. /g' -e 's/<br \/>/ /g' -e 's/, / , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' \
#   -e 's/\?/ \? /g' -e 's/\;/ /g' -e 's/\:/ /g' -e 's/-/ - /g' -e 's/=/ /g' -e 's/=/ /g' -e 's/*/ /g' -e 's/|/ /g' \
#   -e 's/«/ /g' | tr 0-9 " "
# }

mkdir 22m_tweets
cd 22m_tweets

# wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2012.en.shuffled.gz
# wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2013.en.shuffled.gz
# gzip -d news.2012.en.shuffled.gz
# gzip -d news.2013.en.shuffled.gz

# normalize_text < ../data/s3_22m_train_data.txt > data.txt
# normalize_text < ../data/s3_22m_train_data.txt >> data.txt


# gcc ../word2vec.c -o word2vec -lm -pthread -O3 -march=native -funroll-loops
# gcc ../word2phrase.c -o word2phrase -lm -pthread -O3 -march=native -funroll-loops
# gcc ../compute-accuracy.c -o compute-accuracy -lm -pthread -O3 -march=native -funroll-loops
# ./word2phrase -train data.txt -output data-phrase.txt -threshold 200 -debug 2
# ./word2phrase -train data-phrase.txt -output data-phrase2.txt -threshold 100 -debug 2
# ./word2vec -train data-phrase2.txt -output vectors.bin -cbow 1 -size 500 -window 10 -negative 10 -hs 0 -sample 1e-5 -threads 40 -binary 1 -iter 3 -min-count 10
# #./compute-accuracy vectors.bin 400000 < ../questions-words.txt     # should get to almost 78% accuracy on 99.7% of questions
# #./compute-accuracy vectors.bin 1000000 < ../questions-phrases.txt  # about 78% accuracy with 77% coverage
make

time ../word2phrase -train ../data/s3_22m_train_data.txt -output ../data/s3_22m_train_data-norm0-phrase0 -threshold 200 -debug 2
time ../word2phrase -train ../data/s3_22m_train_data-norm0-phrase0 -output ../data/s3_22m_train_data-norm0-phrase1 -threshold 100 -debug 2
tr A-Z a-z < ../data/s3_22m_train_data-norm0-phrase1 > ../data/s3_22m_train_data-norm1-phrase1
time ../word2vec -train ../data/s3_22m_train_data-norm1-phrase1 -output s3_22m-vectors-phrase.bin -sg 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15
../distance s3_22m-vectors-phrase.bin
