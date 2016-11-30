import os
import re
from collections import Counter
from random import shuffle
from operator import itemgetter

path_src = os.getcwd()
path_data = path_src.replace("src","brown")
path_out = path_src.replace("src","data")
all_file_names = []
for file_path in os.listdir(path_data):
    all_file_names.append(os.path.abspath(file_path).replace("src","brown"))
train_file_names = all_file_names[1:2]
test_file_names = all_file_names[2:3]


def convert_brown(file_names, outfile_name, show_tag=True):
    num_sentences = 0
    tags = Counter()
    fout = open(outfile_name, 'w')
    for fin in file_names:
        print (fin)
        for line in open(fin, 'r'):
            line = line.strip()
            if line and not line.startswith('*'):
                if line.startswith('=='):
                    fout.write('\n\n\n')
                else:
                    if line.startswith('['):
                        line = re.subn(r'(^\[ *|\] *$)','',line)[0]
                    if line:
                        pairs = line.split(' ')
                        for pair in pairs:
                            temp = pair.split('/')
                            if len(temp) == 2:
                                word = temp[0]
                                tag = re.subn(r'\|.+$','',temp[1])[0]
                                tags[tag]+=1
                                if show_tag == True:
                                    fout.write(word+'\t'+tag+'\n')
                                else:
                                    fout.write(word+'\n')
                    num_sentences+=1
                    fout.write("\n")

    print("Number Sentences: %d"%num_sentences)
    fout.close()
def count_sentences(file_names):
    print("Counting Sentences")
    num_sentences = 0
    for fin in file_names:
        for line in open(fin, 'r'):
            line = line.strip()
            if line and not line.startswith('*'):
                if line.startswith('=='):
                    print("Start ===")
                else:
                    num_sentences += 1
    print("Number Sentences: %d" % num_sentences)
    return num_sentences

def split_brown(file_names, test_file_name="test", train_file_name="train", percent=0.8):
    print("Split data to train and test")
    num_sentences = count_sentences(file_names)
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
    train_file = open(train_file_name, 'w')

    index_sentence = 0
    for fin in file_names:
        for line in open(fin, 'r'):
            line = line.strip()
            if line and not line.startswith('*'):
                if line.startswith('=='):
                    if sep_dic[index_sentence]:
                        train_file.write('\n\n\n')
                    else:
                        test_file.write('\n\n\n')
                else:
                    if line.startswith('['):
                        line = re.subn(r'(^\[ *|\] *$)','',line)[0]
                    if line:
                        pairs = line.split(' ')
                        for pair in pairs:
                            temp = pair.split('/')
                            if len(temp) == 2:
                                word = temp[0]
                                tag = re.subn(r'\|.+$','',temp[1])[0]
                                if sep_dic[index_sentence]:
                                    train_file.write(word+'\t'+tag+'\n')
                                else:
                                    test_file.write(word+'\t'+tag+'\n')
                                tags[tag]+=1
                                dictionary[word]+=1
                if sep_dic[index_sentence]:
                    train_file.write('\n')
                else:
                    test_file.write('\n')
                index_sentence += 1
    test_file.close()
    train_file.close()

    with open('tags', 'w') as filw:
        for (word, count) in tags.most_common():
            filw.write(word + "\t" + str(count)+"\n")

    filw.close()

    with open('dictionary', 'w') as filw2:
        for (word, count) in dictionary.most_common():
            filw2.write(word + "\t" + str(count)+"\n")
    filw.close()

split_brown(all_file_names, test_file_name="test", train_file_name="train", percent=0.8)
convert_brown(test_file_names, os.path.join(path_out,"test_key.txt"))
convert_brown(test_file_names, os.path.join(path_out,"test.txt"), False)
convert_brown(train_file_names,os.path.join(path_out,"train.txt"))
convert_brown(train_file_names,os.path.join(path_out,"train_fortest.txt"), False)
