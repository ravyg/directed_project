make

# time ./word2vec -train ./data/only_effs/only_effs.txt -output ./data/only_effs/only_effs_vectors.bin -sg 1 -size 200 -window 5 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15 -classes 500
# ./distance ./data/only_effs/only_effs_vectors.bin

time ./word2phrase -train ./data/only_effs/only_effs.txt -output ./data/only_effs/only_effs-norm0-phrase0 -threshold 200 -debug 2
time ./word2phrase -train ./data/only_effs/only_effs-norm0-phrase0 -output ./data/only_effs/only_effs-norm0-phrase1 -threshold 100 -debug 2
tr A-Z a-z < ./data/only_effs/only_effs-norm0-phrase1 > ./data/only_effs/only_effs-norm1-phrase1

time ./word2vec -train ./data/only_effs/only_effs-norm1-phrase1 -output ./data/only_effs/only_effs-vectors-phrase.bin -sg 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15 -classes 500
# ./distance ./data/only_effs/only_effs-vectors-phrase.bin
# ./word-analogy ./data/only_effs/only_effs-vectors-phrase.bin


time ./word2vec -train ./data/only_effs/only_effs-norm1-phrase1 -output ./data/only_effs/only_effs-norm1-phrase1-classes.txt -sg 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -classes 500

sort ./data/only_effs/only_effs-norm1-phrase1-classes.txt -k 2 -n > ./data/only_effs/only_effs-norm1-phrase1-classes.sorted.txt
echo The word classes were saved to file ./data/only_effs/only_effs-norm1-phrase1-classes.sorted.txt
