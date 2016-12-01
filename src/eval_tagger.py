#! /usr/bin/python

import sys
from collections import defaultdict

"""
Evaluate tagger output by comparing it to a gold standard file.
Running the script on your tagger output like this
    python eval_tagger.py data_dev.key your_tagger_output.dat
"""


def corpus_iterator(corpus_file, with_logprob = False):
    """
    Get an iterator object over the corpus file. The elements of the
    iterator contain (word, ne_tag) tuples. Blank lines, indicating
    sentence boundaries return (None, None).
    """
    l = corpus_file.readline()
    tagfield = with_logprob and -2 or -1

    try:
        while l:
            line = l.strip()
            if line: # Nonempty line
                # Extract information from line.
                # Each line has the format
                # word ne_tag [log_prob]
                fields = line.split(" ")
                ne_tag = fields[tagfield]
                word = " ".join(fields[:tagfield])
                yield word, ne_tag
            else: # Empty line
                yield (None, None)
            l = corpus_file.readline()
    except IndexError:
        sys.stderr.write("Could not read line: \n")
        sys.stderr.write("\n%s" % line)
        if with_logprob:
            sys.stderr.write("Did you forget to output log probabilities in the prediction file?\n")
        sys.exit(1)


class Evaluator(object):

    def __init__(self):
        self.sentences = 0
        self.tags_dict = defaultdict(int)
        self.tags = 0
        self.correct_tags=0

    def compare(self, file_gold_standard, file_prediction):
        """
        Compare the prediction against a gold standard. Both objects must be
        generator or iterator objects that return a (word, ne_tag) tuple at a
        time.
        """
        line_data = file_gold_standard.readline()
        line_pre = file_prediction.readline()
        while line_data:
            line_data = line_data.strip()
            line_pre = line_pre.strip()
            if line_data:
                fields = line_data.split(" ")
                pre_fields = line_pre.split(" ")
                data_tag = fields[-1]
                pre_tag = pre_fields[-1]
                word = " ".join(fields[:-1])
                self.tags_dict[word]+=1
                if data_tag == pre_tag:
                    self.correct_tags += 1
                self.tags +=1
            else:
                self.sentences+=1
            line_data = file_gold_standard.readline()
            line_pre = file_prediction.readline()

    def print_scores(self):
        """
        Output a table with accuracy, precision, recall and F1 score.
        """
        print ("Found %d Sentences which %d Tags." % (self.sentences, len(self.tags_dict.keys())))
        print ("Evaluate in %d Tags which Correct: %d Tags." % (self.tags, self.correct_tags))
        print ("Accurace : %.04f \n" % (float(self.correct_tags)/self.tags))
if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.compare(open(sys.argv[1]), open(sys.argv[2]))
    evaluator.print_scores()
