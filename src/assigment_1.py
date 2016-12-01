from hmm import ViterbiTagger
import util


DEBUG = False


def train(train_data_filename, rare_train_data_filename, hmm_model_filename, rare_words_rule):
    print ('1. train hmm model')
    hmm_model = ViterbiTagger(3)
    hmm_model.rare_words_rule = rare_words_rule
    hmm_model.train(open(train_data_filename,'r'))

    print ('2. process rare words')
    util.process_rare_words(
        open(train_data_filename,'r'),
        open(rare_train_data_filename, 'w'),
        hmm_model.rare_words,
        hmm_model.rare_words_rule)

    print ('3. train hmm model again using the new train data')
    hmm_model_rare = ViterbiTagger(3)
    hmm_model_rare.train(open(rare_train_data_filename,'r'))
    hmm_model_rare.write_counts(open(hmm_model_filename, 'w'))


def tag(test_data_filename, result_filename, hmm_model_filename):
    print ('1. load Hmm model')
    tagger = ViterbiTagger(3)
    tagger.read_counts(open(hmm_model_filename,'r'))

    print ('2. tag test file')
    tagger.tag(open(test_data_filename,'r'), open(result_filename, 'w'))


def main():
    TRAIN = True
    # 1. training
    hmm_model_filename = 'hmm.model'
    train_data_filename = 'train_clean'
    rare_train_data_filename = 'rate_train'
    if TRAIN:
        train(train_data_filename, rare_train_data_filename, hmm_model_filename, util.rare_words_rule_p1)

    # 2. tagging
    test_data_filename = 'test_untag_clean'
    result_filename = 'test.output'
    tag(test_data_filename, result_filename, hmm_model_filename)

if __name__ == '__main__':
    main()
