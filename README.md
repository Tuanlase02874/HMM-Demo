==================
HMM-Trigram-Tagger
==================

Requirement
-----------
 - Python 3.5.2
 - six==1.10.0
 
Examples
=============
1. Create data for training and testing HMM: cd \src | python ultils.py
   Functions:
	* Seperate base on name file
		- Create data\test.txt [word]
		- Create data\test_key [word tag]
		- Create data\train.txt [word tag]
		- Create data\train_fortest [word]
	* Seperate base on random sentences
		- src\test [word tag]
		- src\test_untag [word]
		- src\train [word tag]
  Output:
  --------------------------------
    Split data to train and test
    Counting Sentences
	Number Sentences: 57335
	Sentences: 57335
	Train Sentences: 45868
	Test Sentences: 11467
  --------------------------------

  
2. Language Modeling: 

