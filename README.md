==================
HMM-Trigram-Tagger
==================

Requirement
-----------
 - Python 3.5.2
 - six==1.10.0
 
Examples
=============
1. Collection and Cleaning Brown Corpus: 
	Input: \brown foldel
	Output: brown.pos file
	# python convert_brown.py
	> Num Sentence: 54192 
2.Create data for training and testing HMM: Ramdom choose 80% for train and 20% for testing
  Input: brown.pos
  Output: test_2, test_2_untag, train_2, tags, dictionary
  --------------------------------
Split data to train and test
Sentences: 54192
 Train Sentences: 43353
 Test Sentences: 10839
Finish split 54192 sentence
  --------------------------------

  
2. Language Modeling: 

