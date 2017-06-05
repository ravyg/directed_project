make

# time ./word2vec -train ./data/1m_supp/1m_supp.txt -output ./data/1m_supp/1m_supp_vectors.bin -sg 1 -size 200 -window 5 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15 -classes 500
#./distance ./data/1m_supp/1m_supp_vectors.bin

time ./word2phrase -train ./data/1m_supp/1m_supp.txt -output ./data/1m_supp/1m_supp-norm0-phrase0 -threshold 200 -debug 2
time ./word2phrase -train ./data/1m_supp/1m_supp-norm0-phrase0 -output ./data/1m_supp/1m_supp-norm0-phrase1 -threshold 100 -debug 2
tr A-Z a-z < ./data/1m_supp/1m_supp-norm0-phrase1 > ./data/1m_supp/1m_supp-norm1-phrase1

time ./word2vec -train ./data/1m_supp/1m_supp-norm1-phrase1 -output ./data/1m_supp/1m_supp-vectors-phrase.bin -sg 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15 -classes 500
#./distance ./data/1m_supp/1m_supp-vectors-phrase.bin
#./word-analogy ./data/1m_supp/1m_supp-vectors-phrase.bin


time ./word2vec -train ./data/1m_supp/1m_supp-norm1-phrase1 -output ./data/1m_supp/1m_supp-norm1-phrase1-classes.txt -sg 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -classes 500

sort ./data/1m_supp/1m_supp-norm1-phrase1-classes.txt -k 2 -n > ./data/1m_supp/1m_supp-norm1-phrase1-classes.sorted.txt
echo The word classes were saved to file ./data/1m_supp/1m_supp-norm1-phrase1-classes.sorted.txt
