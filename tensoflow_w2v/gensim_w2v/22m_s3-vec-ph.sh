make

time ./word2vec -train ./data/22m_s3/22m_s3.txt -output ./data/22m_s3/22m_s3_vectors.bin -sg 1 -size 200 -window 5 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15 -classes 500
#./distance ./data/22m_s3/22m_s3_vectors.bin

time ./word2phrase -train ./data/22m_s3/22m_s3.txt -output ./data/22m_s3/22m_s3-norm0-phrase0 -threshold 200 -debug 2
time ./word2phrase -train ./data/22m_s3/22m_s3-norm0-phrase0 -output ./data/22m_s3/22m_s3-norm0-phrase1 -threshold 100 -debug 2
tr A-Z a-z < ./data/22m_s3/22m_s3-norm0-phrase1 > ./data/22m_s3/22m_s3-norm1-phrase1
time ./word2vec -train ./data/22m_s3/22m_s3-norm1-phrase1 -output ./data/22m_s3/22m_s3-vectors-phrase.bin -sg 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15 -classes 500
#./distance ./data/22m_s3/22m_s3-vectors-phrase.bin
#./word-analogy ./data/22m_s3/22m_s3-vectors-phrase.bin


time ./word2vec -train ./data/22m_s3/22m_s3-norm1-phrase1 -output ./data/22m_s3/22m_s3-norm1-phrase1-classes.txt -sg 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -classes 500
sort ./data/22m_s3/22m_s3-norm1-phrase1-classes.txt -k 2 -n > ./data/22m_s3/22m_s3-norm1-phrase1-classes.sorted.txt
echo The word classes were saved to file ./data/22m_s3/22m_s3-norm1-phrase1-classes.sorted.txt
