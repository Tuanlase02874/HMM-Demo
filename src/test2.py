from __future__ import division
from collections import defaultdict
from os.path import exists
from count_freqs import Hmm
from eval_tagger import corpus_iterator, Evaluator


def combinations(list_a, list_b):
    for a in list_a:
        for b in list_b:
            yield (a, b)


class GeneTagger:
    def __init__(self, counts_path):
        self.word_count = defaultdict(int)
        self.tag_word = defaultdict(int)

        self.unigram = defaultdict(int)
        self.bigram = defaultdict(int)
        self.trigram = defaultdict(int)

        for line in open(counts_path):
            t = line.strip().split()
            count, label, key = int(t[0]), t[1], tuple(t[2:])
            if label == "1-GRAM":
                self.unigram[key[0]] = count
            elif label == "2-GRAM":
                self.bigram[key] = count
            elif label == "3-GRAM":
                self.trigram[key] = count
            elif label == "WORDTAG":
                self.word_count[key[1]] += count
                self.tag_word[key] = count

        self.tags = self.unigram.keys()

        for word, count in self.word_count.items():
            if count < 5:
                for tag in self.tags:
                    self.tag_word[(tag, '_RARE_')] += self.tag_word[(tag, word)]

    Vo_size = 50000
    def smothing_unigram(self,w):
        lambda_1 = 0.4
        q_ml_1 = lambda_1 * self.unigram[w] + (1 - lambda_1)
        return q_ml_1
    def smothing_unigram(self,w):
        lambda_2 = 0.4
        q_ml_1 = lambda_2 * self.unigram[w] + (1 - lambda_1)
        return q_ml_1


    def q(self, s, u, v):
        "Probability of the trigram (u, v, s) given the prefix bigram (u, v)"
        Vo_size = 50000
        lambda_1 = 0.4
        lambda_2 = 0.4
        lambda_3 = 0.3
        #q = lambda_1*p(s|u,v) + lambda_2*p()
        q_ml_1 = lambda_1*self.unigram[s]/Vo_size + (1-lambda_1)/Vo_size
        q_ml_2 = lambda_2*
        print("%s %s %s"%(u,v,s))
        print (self.trigram[(u, v, s)])
        print  (self.bigram[(u, v)])
        q_ml_s =
        return self.trigram[(u, v, s)] / self.bigram[(u, v)]

    def e(self, word, tag):
        "Probability of the tag emitting the word"
        if tag in ["*", "STOP"]: return 0.0
        if self.word_count[word] < 5: word = '_RARE_'

        return self.tag_word[(tag, word)] / self.unigram[tag]

    def unigram_tagger(self, sentence):
        return [max([(self.e(word, tag), tag) for tag in self.tags])[1]
                for word in sentence]

    def K(self, k):
        if k in (-1, 0): return ["*"]
        return self.tags

    def viterbi_tagger(self, sentence):
        print(sentence)
        # Cleanup method calls
        K, q, e = self.K, self.q, self.e

        # Stores in bp the most likely tag (w) at position (k), for all the
        # possible combinations of tag bigram (u, v) at position (k+1, k+2)
        # pi is the maximum probability for any sequence of length k, ending in
        # the tag bigram (u, v)
        x, n = [""] + sentence, len(sentence)
        pi, bp = {(0, "*", "*"): 1.0}, {}
        for k in range(1, n + 1):
            for u, v in combinations(K(k - 1), K(k)):
                pi[(k, u, v)], bp[(k, u, v)] = max([(
                                                        pi[(k - 1, w, u)] * q(v, w, u) * e(x[k], v),
                                                        w
                                                    ) for w in K(k - 2)])

        # Get the most likely ending tag bigram among all the possible (u, v)
        # combinations, then use these values to start following the back
        # pointers
        y = [""] * (n + 1)
        _, (y[n - 1], y[n]) = max([(
                                       pi[(n, u, v)] * q("STOP", u, v),
                                       (u, v)
                                   ) for u, v in combinations(K(n - 1), K(n))])
        for k in range(n - 2, 0, -1):
            y[k] = bp[(k + 2, y[k + 1], y[k + 2])]
        return y[1:n + 1]


def gen_counts(input_path, output_path):
    if exists(output_path): return

    print('Generating counts from: "%s"' % input_path)
    counter = Hmm(3)
    counter.train(open(input_path, 'r'))
    counter.write_counts(open(output_path, 'w'))


def read_sentence(f):
    sentence = []
    for line in f.readlines():
        if line != '\n':
            sentence.append(line.strip())
        else:
            yield sentence
            sentence = []


def write_tagged_sentence(f, tagged_sentence):
    for word, tag in tagged_sentence:
        f.write("%s %s\n" % (word, tag))
    f.write("\n")


def tag_sentences(tagger, tagger_name, input_path, output_path):
    tagger_method = getattr(tagger, tagger_name + '_tagger')
    with open(input_path, 'r') as in_f, open(output_path, 'wb') as out_f:
        for sentence in read_sentence(in_f):
            write_tagged_sentence(out_f, zip(sentence, tagger_method(sentence)))


def check_tagger(reference_path, dev_path):
    gs_iterator = corpus_iterator(open(reference_path))
    pred_iterator = corpus_iterator(open(dev_path), with_logprob=False)
    evaluator = Evaluator()
    evaluator.compare(gs_iterator, pred_iterator)
    evaluator.print_scores()


if __name__ == '__main__':
    gen_counts('train', 'data.counts')
    tagger = GeneTagger('data.counts')
    tag_sentences(tagger, 'viterbi', 'test_untag', 'data.dev.out')