from collections import Counter
from random import shuffle
import re

def split_brown(file_names="brown.pos", num_sentences =54192, test_file_name="test", train_file_name="train", percent=0.8):
    print("Split data to train and test")
    print("Sentences: %d"%num_sentences)
    num_sentences_train = int(percent * num_sentences)
    print (" Train Sentences: %d"% num_sentences_train)
    print (" Test Sentences: %d" % (num_sentences - num_sentences_train))
    index_sentence = [i for i in range(num_sentences)]
    shuffle(index_sentence)
    sep_dic = {}
    for i in index_sentence[:num_sentences_train]:
        sep_dic[i] = True
    for i in index_sentence[num_sentences_train:]:
        sep_dic[i] = False

    tags = Counter()
    dictionary = Counter()

    test_file = open(test_file_name, 'w')
    test_untags_file = open(test_file_name+"_untag", 'w')
    train_file = open(train_file_name, 'w')

    index_sentence = 0


    sentence_words =[]
    for line in open(file_names, 'r'):
        line = line.strip()

        if line == "":
            for (word,tag) in sentence_words:
                if sep_dic[index_sentence]:
                    train_file.write(word + '\t' + tag + '\n')
                else:
                    test_file.write(word + '\t' + tag + '\n')
                    test_untags_file.write(word + '\n')
            if sep_dic[index_sentence]:
                train_file.write('\n')
            else:
                test_file.write('\n')
                test_untags_file.write('\n')
            sentence_words = []
            index_sentence+=1
            if index_sentence == num_sentences:
                print("Finish split %d sentence"% num_sentences)
                break
        else:
            l = line.split("\t")
            sentence_words.append((l[0],l[1]))
            tags[l[1]]+=1
            dictionary[l[0]]+=1

    test_file.close()
    train_file.close()
    test_untags_file.close()

    with open('tags', 'w') as filw:
        for (word, count) in tags.most_common():
            filw.write(word + "\t" + str(count)+"\n")

    filw.close()

    with open('dictionary', 'w') as filw2:
        for (word, count) in dictionary.most_common():
            filw2.write(word + "\t" + str(count)+"\n")
    filw.close()

split_brown(file_names="brown.pos", num_sentences =54192, test_file_name="test_2", train_file_name="train_2", percent=0.8)
