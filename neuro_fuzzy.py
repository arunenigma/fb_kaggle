# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

import itertools
from operator import itemgetter


class NeuroFuzzySystem(object):
    PI_bundle_unigrams = {}
    PI_bundle_bigrams = {}
    PI_bundle_trigrams = {}

    def __init__(self):
        self.word_list = []
        self.cog_list = []
        self.word_info = {}

        self.bigram_list = []
        self.cog_list_bigrams = []
        self.bigram_info = {}

        self.trigram_list = []
        self.cog_list_trigrams = []
        self.trigram_info = {}

        self.PI_bundle_unigrams = {}
        self.PI_bundle_bigrams = {}
        self.PI_bundle_trigrams = {}

        self.mfs = []

    def neuroFuzzyModelling(self, tf_idf_list, u1, u2, u13, u14,
                            tf_idf_bigram_list,
                            b1, b2, b3, b4, b5, tf_idf_trigram_list, t1, t2, t3, t4, t5, t6):
        """
        @param tf_idf_list: list of unigrams with info like tf_idf, location index and location signature
        @param tf_idf_bigram_list:
        @param tf_idf_trigram_list:
        """

        out = open('out.txt', 'w')
        for item in u1:
            out.write(str(item[0]) + " " + str(item[1]) + '\n')
        out.close()

        # dictionary of word bag names
        bag_names = {'u1': 'common English word', 'u2': 'unigram noun', 'u3': 'unigram link tag',
                     'u4': 'unigram heading H1 tag', 'u5': 'unigram heading H2 tag', 'u6': 'unigram heading H3 tag',
                     'u7': 'unigram heading H4 tag', 'u8': 'unigram heading H5 tag', 'u9': 'unigram heading H6 tag',
                     'u10': 'unigram LI Title tag', 'u11': 'unigram TD tag', 'u12': 'unigram TH tag',
                     'u13': 'unigram all CAP', 'u14': 'unigram number', 'dd_o': 'object', 'dd_f': 'feature',
                     'dd_a': 'attribute'}

        u1 = {item[0]: item[1:] for item in u1}  # word bag - common english words
        u2 = {item[0]: item[1:] for item in u2}
        u13 = {item[0]: item[1:] for item in u13}
        u14 = {item[0]: item[1:] for item in u14}

        b1 = {item[0]: item[1:] for item in b1}
        b2 = {item[0]: item[1:] for item in b2}
        b3 = {item[0]: item[1:] for item in b3}
        b4 = {item[0]: item[1:] for item in b4}
        b5 = {item[0]: item[1:] for item in b5}

        t1 = {item[0]: item[1:] for item in t1}
        t2 = {item[0]: item[1:] for item in t2}
        t3 = {item[0]: item[1:] for item in t3}
        t4 = {item[0]: item[1:] for item in t4}
        t5 = {item[0]: item[1:] for item in t5}
        t6 = {item[0]: item[1:] for item in t6}

        for info, word in tf_idf_list.iteritems():

            try:
                activated_fuzzy_sets = []
                u1_nrn_info = u1.get(word, 0)
                if not u1_nrn_info == 0:
                    activated_fuzzy_sets.append(bag_names.get('u1'))
                u2_nrn_info = u2.get(word, 0)
                if not u2_nrn_info == 0:
                    activated_fuzzy_sets.append(bag_names.get('u2'))
                u13_nrn_info = u13.get(word, 0)
                if not u13_nrn_info == 0:
                    activated_fuzzy_sets.append(bag_names.get('u13'))
                u14_nrn_info = u14.get(word, 0)
                if not u14_nrn_info == 0:
                    activated_fuzzy_sets.append(bag_names.get('u14'))

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            #print word
            #print activated_fuzzy_sets

            if not u1_nrn_info == 0:
                u1_mf1 = u1_nrn_info[1] * u1_nrn_info[2] - 1
                u1_mf2 = u1_nrn_info[3] * u1_nrn_info[4] - 1
                self.mfs.append([u1_mf1, u1_mf2])
                self.wts.append(u1_nrn_info[2])
                self.wts.append(u1_nrn_info[4])

            if not u2_nrn_info == 0:
                u2_mf1 = u2_nrn_info[1] * u2_nrn_info[2] + 1  # +1 --> bias
                u2_mf2 = u2_nrn_info[3] * u2_nrn_info[4] + 1
                self.mfs.append([u2_mf1, u2_mf2])
                self.wts.append(u2_nrn_info[2])
                self.wts.append(u2_nrn_info[4])

            if not u13_nrn_info == 0:
                u13_mf1 = u13_nrn_info[1] * u13_nrn_info[2] + 2
                u13_mf2 = u13_nrn_info[3] * u13_nrn_info[4] + 2
                self.mfs.append([u13_mf1, u13_mf2])
                self.wts.append(u13_nrn_info[2])
                self.wts.append(u13_nrn_info[4])

            if not u14_nrn_info == 0:
                u14_mf1 = u14_nrn_info[1] * u14_nrn_info[2]
                u14_mf2 = u14_nrn_info[3] * u14_nrn_info[4]
                self.mfs.append([u14_mf1, u14_mf2])
                self.wts.append(u14_nrn_info[2])
                self.wts.append(u14_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyUnigrams(word, rule_inputs, weights, info)

        # ****************** BIGRAMS *******************
        for info, bigram, in tf_idf_bigram_list.iteritems():
            try:
                b1_nrn_info = b1.get(bigram, 0)
                b2_nrn_info = b2.get(bigram, 0)
                b3_nrn_info = b3.get(bigram, 0)
                b4_nrn_info = b4.get(bigram, 0)
                b5_nrn_info = b5.get(bigram, 0)

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not b1_nrn_info == 0:
                b1_mf1 = b1_nrn_info[1] * b1_nrn_info[2]
                b1_mf2 = b1_nrn_info[3] * b1_nrn_info[4]
                self.mfs.append([b1_mf1, b1_mf2])
                self.wts.append(b1_nrn_info[2])
                self.wts.append(b1_nrn_info[4])

            if not b2_nrn_info == 0:
                b2_mf1 = b2_nrn_info[1] * b2_nrn_info[2]
                b2_mf2 = b2_nrn_info[3] * b2_nrn_info[4]
                self.mfs.append([b2_mf1, b2_mf2])
                self.wts.append(b2_nrn_info[2])
                self.wts.append(b2_nrn_info[4])

            if not b3_nrn_info == 0:
                b3_mf1 = b3_nrn_info[1] * b3_nrn_info[2]
                b3_mf2 = b3_nrn_info[3] * b3_nrn_info[4]
                self.mfs.append([b3_mf1, b3_mf2])
                self.wts.append(b3_nrn_info[2])
                self.wts.append(b3_nrn_info[4])

            if not b4_nrn_info == 0:
                b4_mf1 = b4_nrn_info[1] * b4_nrn_info[2]
                b4_mf2 = b4_nrn_info[3] * b4_nrn_info[4]
                self.mfs.append([b4_mf1, b4_mf2])
                self.wts.append(b4_nrn_info[2])
                self.wts.append(b4_nrn_info[4])

            if not b5_nrn_info == 0:
                b5_mf1 = b5_nrn_info[1] * b5_nrn_info[2]
                b5_mf2 = b5_nrn_info[3] * b5_nrn_info[4]
                self.mfs.append([b5_mf1, b5_mf2])
                self.wts.append(b5_nrn_info[2])
                self.wts.append(b5_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyBigrams(bigram, rule_inputs, weights, info)

        # ****************** TRIGRAMS *******************
        for info, trigram, in tf_idf_trigram_list.iteritems():
            try:
                t1_nrn_info = t1.get(trigram, 0)
                t2_nrn_info = t2.get(trigram, 0)
                t3_nrn_info = t3.get(trigram, 0)
                t4_nrn_info = t4.get(trigram, 0)
                t5_nrn_info = t5.get(trigram, 0)
                t6_nrn_info = t6.get(trigram, 0)

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not t1_nrn_info == 0:
                t1_mf1 = t1_nrn_info[1] * t1_nrn_info[2]
                t1_mf2 = t1_nrn_info[3] * t1_nrn_info[4]
                self.mfs.append([t1_mf1, t1_mf2])
                self.wts.append(t1_nrn_info[2])
                self.wts.append(t1_nrn_info[4])

            if not t2_nrn_info == 0:
                t2_mf1 = t2_nrn_info[1] * t2_nrn_info[2]
                t2_mf2 = t2_nrn_info[3] * t2_nrn_info[4]
                self.mfs.append([t2_mf1, t2_mf2])
                self.wts.append(t2_nrn_info[2])
                self.wts.append(t2_nrn_info[4])

            if not t3_nrn_info == 0:
                t3_mf1 = t3_nrn_info[1] * t3_nrn_info[2]
                t3_mf2 = t3_nrn_info[3] * t3_nrn_info[4]
                self.mfs.append([t3_mf1, t3_mf2])
                self.wts.append(t3_nrn_info[2])
                self.wts.append(t3_nrn_info[4])

            if not t4_nrn_info == 0:
                t4_mf1 = t4_nrn_info[1] * t4_nrn_info[2]
                t4_mf2 = t4_nrn_info[3] * t4_nrn_info[4]
                self.mfs.append([t4_mf1, t4_mf2])
                self.wts.append(t4_nrn_info[2])
                self.wts.append(t4_nrn_info[4])

            if not t5_nrn_info == 0:
                t5_mf1 = t5_nrn_info[1] * t5_nrn_info[2]
                t5_mf2 = t5_nrn_info[3] * t5_nrn_info[4]
                self.mfs.append([t5_mf1, t5_mf2])
                self.wts.append(t5_nrn_info[2])
                self.wts.append(t5_nrn_info[4])

            if not t6_nrn_info == 0:
                t6_mf1 = t6_nrn_info[1] * t6_nrn_info[2]
                t6_mf2 = t6_nrn_info[3] * t6_nrn_info[4]
                self.mfs.append([t6_mf1, t6_mf2])
                self.wts.append(t6_nrn_info[2])
                self.wts.append(t6_nrn_info[4])
            
            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyTrigrams(trigram, rule_inputs, weights, info)

    def defuzzifyUnigrams(self, word, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.word_list.append(word)
        self.cog_list.append(cog)
        self.word_info[info] = word

    def defuzzifyBigrams(self, bigram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.bigram_list.append(bigram)
        self.cog_list_bigrams.append(cog)
        self.bigram_info[info] = bigram

    def defuzzifyTrigrams(self, trigram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.trigram_list.append(trigram)
        self.cog_list_trigrams.append(cog)
        self.trigram_info[info] = trigram

    def normCOGUnigrams(self):
        for k, v in self.word_info.iteritems():
            print k, v

        if not len(self.cog_list) < 1:
            self.max_cog = max(self.cog_list)
            self.cog_list = [cog / self.max_cog for cog in self.cog_list]
            word_rank = dict(zip(self.word_list, self.cog_list))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** UNIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.uni_gram_lv_list = []
                self.uni_gram_lv_list.append(item[1])  # item[1] --> PI score
                for info, word in self.word_info.iteritems():
                    if item[0] == word:
                        print info
                        self.uni_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_unigrams[item[0]] = self.uni_gram_lv_list

        else:
            print '*********** UNIGRAMS ***********'
            print None

    def normCOGBigrams(self):
        if not len(self.cog_list_bigrams) < 1:
            print self.cog_list_bigrams
            max_cog = max(self.cog_list_bigrams)
            self.cog_list_bigrams = [cog / max_cog for cog in self.cog_list_bigrams]
            word_rank = dict(zip(self.bigram_list, self.cog_list_bigrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** BIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.bi_gram_lv_list = []
                self.bi_gram_lv_list.append(item[1])
                for info, bigram in self.bigram_info.iteritems():
                    if item[0] == bigram:
                        print info
                        self.bi_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_bigrams[item[0]] = self.bi_gram_lv_list
        else:
            print '*********** BIGRAMS ***********'
            print None

    def normCOGTrigrams(self):
        if not len(self.cog_list_trigrams) < 1:
            max_cog = max(self.cog_list_trigrams)
            self.cog_list_trigrams = [cog / max_cog for cog in self.cog_list_trigrams]
            word_rank = dict(zip(self.trigram_list, self.cog_list_trigrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** TRIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.tri_gram_lv_list = []
                self.tri_gram_lv_list.append(item[1])
                for info, trigram in self.trigram_info.iteritems():
                    if item[0] == trigram:
                        print info
                        self.tri_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_trigrams[item[0]] = self.tri_gram_lv_list
        else:
            print '*********** TRIGRAMS ***********'
            print None