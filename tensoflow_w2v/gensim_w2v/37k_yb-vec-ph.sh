# mkdir 37k_yb
# cd 37m_yb

make

time ./word2vec -train ./data/run2/37k_yb_sup_cleaned.txt -output ./data/run2/37k_yb_sup_vectors.bin -sg 1 -size 200 -window 5 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15 -classes 500
# ./distance ./data/run2/37k_yb_sup_vectors.bin

time ./word2phrase -train ./data/run2/37k_yb_sup_cleaned.txt -output ./data/run2/37k_yb_sup_cleaned-norm0-phrase0 -threshold 200 -debug 2
time ./word2phrase -train ./data/run2/37k_yb_sup_cleaned-norm0-phrase0 -output ./data/run2/37k_yb_sup_cleaned-norm0-phrase1 -threshold 100 -debug 2
tr A-Z a-z < ./data/run2/37k_yb_sup_cleaned-norm0-phrase1 > ./data/run2/37k_yb_sup_cleaned-norm1-phrase1
time ./word2vec -train ./data/run2/37k_yb_sup_cleaned-norm1-phrase1 -output ./data/run2/37k_yb_sup-vectors-phrase.bin -sg 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15 -classes 500
# ./distance ./data/run2/37k_yb_sup-vectors-phrase.bin
# ./word-analogy ./data/run2/37k_yb_sup-vectors-phrase.bin


time ./word2vec -train ./data/run2/37k_yb_sup_cleaned-norm1-phrase1 -output ./data/run2/37k_yb_sup_cleaned-norm1-phrase1-classes.txt -sg 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -classes 500
sort ./data/run2/37k_yb_sup_cleaned-norm1-phrase1-classes.txt -k 2 -n > ./data/run2/37k_yb_sup_cleaned-norm1-phrase1-classes.sorted.txt
echo The word classes were saved to file ./data/run2/37k_yb_sup_cleaned-norm1-phrase1-classes.sorted.txt
