U.S-Presidential-Speeches
=========================


This is an attempt to analyse text of U.S. President's Speeches from 1790 to 2006 using Word2Vec model in gensim. 

- Data in enclosed here as speech.txt
- all_speech.txt is the processed version of the speeches such that each line contains one processed speeches
- data_processed.txt is the text file of json.dumps() containing full metadata from speech.txt in the form of list of dictionaries
      - 'who' : President's name
      - 'date' : date of speech (example : January 27, 1984)
      - 'speech' : Full speech
      - 'what' :'State of the Union Address'

- speech.py contains code to process speech.txt
- w2v_speech.py contains gensim model to learn w2v model of the from speeches. Here I have assumed one speech to constitute one sentence.
Speech vector is then calculated by averaging all the word vectors in the speech
- w2v_tsne.py contains the code to plot 2D version of 100 dimensional speech vectors
- speech_vectors.npy is numpy vector of all speeches as processed in w2v_tsne.py
- .png files are respective tsne plots of speech vectors


Here is the t-SNE plot of speech vectors:
! [alt tag](https://github.com/prateekpg2455/U.S-Presidential-Speeches/blob/master/plot_without_labels.png)

