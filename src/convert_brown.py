# -*- coding: utf-8 -*-
import re
import os

path_src = os.getcwd()
BROWN_POS_PATH = path_src.replace("src","brown\\")

# The separator you want to use in the generated brown.pos
TAG_TOKEN_SEPARATOR = "\t"

out  = open("brown.pos","w")
tokens_pattern = re.compile('(\s*[(.+)/(.+)]\s+)*')

files = os.listdir(BROWN_POS_PATH)

sentence_lines = []
num_sentence = 0
for filename in files:
    if len(filename)==4 and filename[0] == 'c':
        print ('Parsing '+filename+'...')
        file = open(BROWN_POS_PATH+filename)
        ignore_sentence = False
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                tokens = line.split(' ')
                if len(tokens)>4:
                    for token_str in tokens:
                        parts = token_str.split('/')
                        if len(parts)!=2:
                           continue
                        token = parts[0].strip()
                        tag = parts[1].strip()
                        if tag == "``" or tag == "''":
                            continue

                        if tag.endswith('-nc') or tag.endswith('+vb') or tag.endswith('+ppss') or tag.endswith('+cs'):
                            ignore_sentence = True
                        if tag[:2] == 'fw' or tag.endswith('-hl'):
                            tag = 'fw'
                        if tag.endswith('-tl'):
                            tag = tag[:-3]

                        token_already_added = False

                        if tag.endswith('+ber'):
                            sentence_lines.append(token.replace("'re","") + TAG_TOKEN_SEPARATOR + tag[:-4] + "\n")
                            sentence_lines.append("are" + TAG_TOKEN_SEPARATOR + "ber" + "\n")
                            token_already_added = True

                        if tag.endswith('+bem'):
                            sentence_lines.append(token.replace("'m","") + TAG_TOKEN_SEPARATOR + tag[:-4] + "\n")
                            sentence_lines.append("am" + TAG_TOKEN_SEPARATOR + "bem" + "\n")
                            token_already_added = True

                        if not token_already_added:
                            sentence_lines.append(token + TAG_TOKEN_SEPARATOR + tag + "\n")

                if len(sentence_lines)>0 and not ignore_sentence:
                    out.write(''.join(sentence_lines))
                    out.write('\n')
                    num_sentence+=1

                ignore_sentence = False
                sentence_lines = []
out.close()
print("Num Sentence: %d "% num_sentence)