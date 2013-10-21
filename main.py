# -*- coding: utf-8 -*-

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from range_estimator import RangeCalculator
from neuro_fuzzy import NeuroFuzzySystem
from dom import DegreeOfMembership
from ques_analyzer import *
from read import *
import itertools


if __name__ == '__main__':
    hd5_file = pandas.HDFStore('Train.h5', 'w')
    csv_file = read_csv('Train.csv', iterator=True, chunksize=10)
    read = ReadData()
    read.chunkAndDataStreamData(hd5_file, csv_file)
    ids = read.ids
    titles = read.titles
    bodies = read.bodies
    tags = read.tags
    ques_count = 0
    ques_word_count_list, corpus_words = [], []
    ques_bi_gram_count_list, corpus_bi_grams = [], []
    ques_tri_gram_count_list, corpus_tri_grams = [], []

    for ID, title, body, tag in itertools.izip(ids, titles, bodies, tags):
        body = '<question><title>' + title[0] + '</title><tag>' + tag.tolist()[0] + '</tag>' + body[0].strip().replace('\n', '') + '</question>'
        ques_words = []
        bi_grams = []
        tri_grams = []

        cor = Corpus(body, ques_words, bi_grams, tri_grams)
        cor.generateLocationVector(cor.parseXML(), [0])
        ques_count += 1

        ques_word_count = len(ques_words)
        ques_word_count_list.append(ques_word_count)
        corpus_words.append(ques_words)

        ques_bi_gram_count = len(bi_grams)
        ques_bi_gram_count_list.append(ques_bi_gram_count)
        corpus_bi_grams.append(bi_grams)

        ques_tri_gram_count = len(tri_grams)
        ques_tri_gram_count_list.append(ques_tri_gram_count)
        corpus_tri_grams.append(tri_grams)

    corpus = []
    for words in corpus_words:
        for word in words:
            corpus.append(word)

    corpus_bigrams = []
    for bigrams in corpus_bi_grams:
        for bigram in bigrams:
            corpus_bigrams.append(bigram)

    corpus_trigrams = []
    for trigrams in corpus_tri_grams:
        for trigram in trigrams:
            corpus_trigrams.append(trigram)

    # ***************************************************************************
    #              Each StackOverflow question is run against the corpus
    # ***************************************************************************
    for ID, title, body, tag in itertools.izip(ids, titles, bodies, tags):
        body = '<question><title>' + title[0] + '</title><tag>' + tag.tolist()[0] + '</tag>' + body[0].strip().replace('\n', '') + '</question>'
        ques_ID = 0
        ques_words = []
        bi_grams = []
        tri_grams = []

        loc_vec = LocationVector(body, ques_words, bi_grams, tri_grams)
        loc_vec.generateLocationVector(loc_vec.parseXML(), [0])

        ques_ID += 1
        statement_facts_data = []

        tagger = WordTagger(ques_ID, body, ques_words, bi_grams,
                            tri_grams, corpus, corpus_bigrams,
                            corpus_trigrams, ques_count, ques_word_count_list,
                            ques_bi_gram_count_list, ques_tri_gram_count_list)
        tagger.generateLocationVector(tagger.parseXML(), [0])

        # ------------- Word Bags ------------

        # tfidf info list of N-grams
        tf_idf_list = tagger.tf_idf_list  # all ques words (unique)
        tf_idf_bigram_list = tagger.tf_idf_bigram_list
        tf_idf_trigram_list = tagger.tf_idf_trigram_list

        # word bags Unigrams
        tf_idf_common_eng_words = tagger.common_eng_words  # common english excluding stopwords and words whose IDF = 1
        tf_idf_nouns_unigrams = tagger.nouns_unigrams  # uni-gram nouns excluding stopwords and words whose IDF = 1
        tf_idf_loc_sig_code = tagger.loc_sig_code_unigrams  # uni-grams whose location signature is "code"
        tf_idf_loc_sig_p = tagger.loc_sig_p_unigrams  # uni-grams whose location signature is "p"
        tf_idf_loc_sig_pre = tagger.loc_sig_pre_unigrams  # uni-grams whose location signature is "p"
        tf_idf_loc_sig_a = tagger.loc_sig_a_unigrams  # uni-grams whose location signature is "p"
        tf_idf_all_cap_unigrams = tagger.all_caps_unigrams
        tf_idf_numbers_unigrams = tagger.numbers_unigrams

        # ------------ word bags Bigrams -----------

        tf_idf_bigram_NNP_NNP = tagger.bigram_NNP_NNP  # bi-grams with NNP + NNP POS
        tf_idf_bigram_NNP_NN = tagger.bigram_NNP_NN  # bi-grams with NNP + NN POS
        tf_idf_bigram_NN_NN = tagger.bigram_NN_NN  # bi-grams with NN + NN POS
        tf_idf_bigram_NN_NNS = tagger.bigram_NN_NNS  # bi-grams with NN + NNS POS
        tf_idf_bigram_NN_VBD = tagger.bigram_NN_VBD  # bi-grams with NN + VBD POS

        # ------------ word bags Trigrams -----------

        tf_idf_trigram_NNP_NNP_NNP = tagger.trigram_NNP_NNP_NNP  # tri-grams with NNP + NNP + NNP POS
        tf_idf_trigram_NNP_NNP_NN = tagger.trigram_NNP_NNP_NN  # tri-grams with NNP + NNP + NN POS
        tf_idf_trigram_NNP_NN_NN = tagger.trigram_NNP_NN_NN  # tri-grams with NNP + NN + NN POS
        tf_idf_trigram_NN_NN_NN = tagger.trigram_NN_NN_NN  # tri-grams with NN + NN + NN POS
        tf_idf_trigram_NN_NNS_CD = tagger.trigram_NN_NNS_CD  # tri-grams with NN + NNS + CD POS
        tf_idf_trigram_NN_NN_CD = tagger.trigram_NN_NN_CD  # tri-grams with NN + NN + CD POS

        print tf_idf_loc_sig_code
        print tf_idf_loc_sig_a

        def neuro_fuzzy(x):
            range_span = RangeCalculator()
            range_span.calculateFilterIRange(x)
            #tf_idf_values = range_span.tf_idf_values
            span = range_span.span
            span_pivots = range_span.pivots
            dom = DegreeOfMembership()
            dom.findFuzzySet(x, span, span_pivots)
            y = dom.dom_data_list
            return y

        # ----------------------------------------------------------

        u1 = neuro_fuzzy(tf_idf_common_eng_words)
        u2 = neuro_fuzzy(tf_idf_nouns_unigrams)
        u13 = neuro_fuzzy(tf_idf_all_cap_unigrams)
        u14 = neuro_fuzzy(tf_idf_numbers_unigrams)

        # fuzzy sets for bigrams
        b1 = neuro_fuzzy(tf_idf_bigram_NNP_NNP)
        b2 = neuro_fuzzy(tf_idf_bigram_NNP_NN)
        b3 = neuro_fuzzy(tf_idf_bigram_NN_NN)
        b4 = neuro_fuzzy(tf_idf_bigram_NN_NNS)
        b5 = neuro_fuzzy(tf_idf_bigram_NN_VBD)

        # fuzzy sets for trigrams
        t1 = neuro_fuzzy(tf_idf_trigram_NNP_NNP_NNP)
        t2 = neuro_fuzzy(tf_idf_trigram_NNP_NNP_NN)
        t3 = neuro_fuzzy(tf_idf_trigram_NNP_NN_NN)
        t4 = neuro_fuzzy(tf_idf_trigram_NN_NN_NN)
        t5 = neuro_fuzzy(tf_idf_trigram_NN_NNS_CD)
        t6 = neuro_fuzzy(tf_idf_trigram_NN_NN_CD)

        nf = NeuroFuzzySystem()
        nf.neuroFuzzyModelling(tf_idf_list, u1, u2, u13, u14, tf_idf_bigram_list,
                               b1, b2, b3, b4, b5, tf_idf_trigram_list, t1, t2, t3, t4, t5, t6)

        nf.normCOGUnigrams()
        nf.normCOGBigrams()
        nf.normCOGTrigrams()

        PI_bundle_unigrams = NeuroFuzzySystem.PI_bundle_unigrams
        PI_bundle_bigrams = NeuroFuzzySystem.PI_bundle_bigrams
        PI_bundle_trigrams = NeuroFuzzySystem.PI_bundle_trigrams