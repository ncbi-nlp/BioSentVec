./fasttext skipgram -input $TEXT_DATA -output $MODEL -dim 200 -t 0.001 -minCount 0 -neg 10 -wordNgrams 6 -ws 30
