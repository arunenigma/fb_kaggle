# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

# ques_analyzer.py generates input data for fuzzification

from nltk import corpus as corpus, word_tokenize, pos_tag
from nltk import bigrams, trigrams
from string import maketrans
from lxml import etree
from math import log10
from corpus import *
import enchant
import re


class LocationVector(object):
    def __init__(self, body, ques_words, bi_grams, tri_grams):
        self.body = body
        self.ques_words = ques_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams

    def parseXML(self):
        self.body = self.body.replace('rel="nofollow"', '')
        parser = etree.XMLParser(recover=True)
        f = etree.parse(BytesIO(self.body), parser)
        fstring = etree.tostring(f, pretty_print=True)
        element = etree.fromstring(fstring)
        return element

    def generateLocationVector(self, branch, index):
        if branch.text is not None:
            branch.text = branch.text.encode('ascii', 'ignore')
            if not branch.getchildren():
                sentences = branch.text.split('. ')
                for sentence in range(0, len(sentences)):
                    #sentence_location = (("{0}[{1}]".format(index, sentence)), sentences[sentence])
                    words = sentences[sentence].split()
                    for word in range(0, len(words)):
                        word_location = (("{0}[{1}][{2}]".format(index, sentence, word)), words[word])
                        # any change in line below should be replicated in method generateLocationVector of 
                        # class LocationVector of this file and corpus.py file also
                        symbols = ",[]();:<>+=&+%!@#~?{}|\""
                        whitespace = "                       "
                        replace = maketrans(symbols, whitespace)
                        ques_word = word_location[1].translate(replace)
                        ques_word = ques_word.lstrip()
                        ques_word = ques_word.rstrip()
                        if len(ques_word) > 1 and not len(ques_word) > 16:
                            self.ques_words.append(ques_word)

                    bi_grams = bigrams(words)
                    if not len(bi_grams) < 1:
                        for bi_gram in bi_grams:
                            bi_gram = ' '.join(bi_gram)
                            self.bi_grams.append(bi_gram)

                    tri_grams = trigrams(words)
                    if not len(tri_grams) < 1:
                        for tri_gram in tri_grams:
                            tri_gram = ' '.join(tri_gram)
                            self.tri_grams.append(tri_gram)

            else:
                for subtree in range(0, len(branch)):
                    LocationVector.generateLocationVector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))


class HelperFunctions(object):
    def isNumber(self, s):
        m = re.findall(r"(^[0-9]*[0-9., ]*$)", s)
        return m

    def allLowerCase(self, s):
        m = re.search("[a-z]", s)
        return m

    def percentage(self, a, b):
        return 100 * float(a / b)


class WordTagger(HelperFunctions):
    """
        parse xml and generate location vector
    """
    spell_checker_US = enchant.Dict('en_US')
    spell_checker_GB = enchant.Dict('en_GB')
    spell_checker_AU = enchant.Dict('en_AU')

    def __init__(self, ques_ID, body, ques_words, bi_grams, tri_grams, corpus, corpus_bigrams,
                 corpus_trigrams, ques_count, ques_word_count_list, ques_bi_gram_count_list, ques_tri_gram_count_list):
        super(WordTagger, self).__init__()
        self.word_location = []
        self.ques_ID = ques_ID
        self.body = body

        self.ques_words = ques_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams

        self.corpus = corpus
        self.corpus_bigrams = corpus_bigrams
        self.corpus_trigrams = corpus_trigrams

        self.ques_count = ques_count
        self.ques_word_count_list = ques_word_count_list
        self.ques_bi_gram_count_list = ques_bi_gram_count_list
        self.ques_tri_gram_count_list = ques_tri_gram_count_list

        self.tf_idf_list = {}
        self.tf_idf_bigram_list = {}
        self.tf_idf_trigram_list = {}

        self.ques_domain_dict_match = []
        self.potential_candidates = []

        self.common_eng_words = {}
        self.common_eng_words_UPPER = {}
        self.abbreviation_cluster = {}

        self.nouns_unigrams = {}
        self.verbs_unigrams = {}
        self.all_caps_unigrams = {}
        self.numbers_unigrams = {}

        self.bigram_NNP_NNP = {}
        self.bigram_NNP_NN = {}
        self.bigram_NN_NN = {}
        self.bigram_NN_NNS = {}
        self.bigram_NN_VBD = {}

        self.trigram_NNP_NNP_NNP = {}
        self.trigram_NNP_NNP_NN = {}
        self.trigram_NNP_NN_NN = {}
        self.trigram_NN_NN_NN = {}
        self.trigram_NN_NN_CD = {}
        self.trigram_NN_NNS_CD = {}

        self.loc_sig_p_unigrams = {}
        self.loc_sig_code_unigrams = {}
        self.loc_sig_pre_unigrams = {}
        self.loc_sig_em_unigrams = {}
        self.loc_sig_blockquote_unigrams = {}
        self.loc_sig_ol_unigrams = {}
        self.loc_sig_li_unigrams = {}
        self.loc_sig_a_unigrams = {}

        self.ques_english_dict_match_count = 0
        self.number_match_count = 0
        self.abbreviation_match_count = 0
        self.symbol_match_count = 0
        self.repetitive_word_count = 0

    def parseXML(self):
        self.body = self.body.replace('rel="nofollow"', '')
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        f = etree.parse(BytesIO(self.body), parser)
        fstring = etree.tostring(f, pretty_print=True)
        element = etree.fromstring(fstring)
        return element

    def generateLocationVector(self, branch, index):
        """
            generating location vector for every data in spec
        """
        signature_map = []
        #statement_signature_map = []

        signature = branch.tag
        #print branch.getchildren()
        parent = branch.getparent()

        while True:
            if not parent is None:
                signature_map.append(parent.tag)
                parent = parent.getparent()
                continue
            break

        signature_map.append(signature)
        last = signature_map[-1]
        signature_map = signature_map[-2::-1]
        signature_map.append(last)

        if branch.text is not None:
            branch.text = branch.text.encode('ascii', 'ignore')

            if not branch.getchildren():
                statements = branch.text.split('. ')
                signature_map.append('statement')
                self.statement_signature_map = signature_map
                signature_map.append('word')
                for statement in range(0, len(statements)):
                    statement_location = (("{0}[{1}]".format(index, statement)), statements[statement])
                    words = statements[statement].split()
                    self.statement_loc_vec = statement_location[0]
                    for word in range(0, len(words)):
                        self.word_location = (("{0}[{1}][{2}]".format(index, statement, word)), words[word])
                        # any change in line below should be replicated in method generateLocationVector of 
                        # class LocationVector of this file and corpus.py file also
                        symbols = ",[]();:<>+=&+%!@#~?{}|\""
                        whitespace = "                       "
                        replace = maketrans(symbols, whitespace)
                        ques_word = self.word_location[1].translate(replace)
                        ques_word = ques_word.lstrip()
                        ques_word = ques_word.rstrip()

                        if len(ques_word) > 1 and not len(ques_word) > 16:
                            self.ques_word = ques_word
                            self.ques_word_lower_case = ques_word.lower()
                            self.word_location_index = self.word_location[0].replace('][', ' ')
                            self.word_location_index = self.word_location_index.replace('[', '')
                            self.word_location_index = self.word_location_index.replace(']', '')
                            self.signature_map = signature_map
                            WordTagger.wordMatcher(self)

                    bi_grams = bigrams(words)
                    if not len(bi_grams) < 1:
                        for i, bi_gram in enumerate(bi_grams):
                            self.bi_gram = ' '.join(bi_gram)
                            self.statement_loc_vec = self.statement_loc_vec.replace('][', ' ')
                            self.statement_loc_vec = self.statement_loc_vec.replace('[', '')
                            self.statement_loc_vec = self.statement_loc_vec.replace(']', '')
                            self.bi_gram_index = self.statement_loc_vec + ' ' + str(
                                i) + ' | ' + self.statement_loc_vec + ' ' + str(i + 1)
                            WordTagger.wordMatcherBigram(self, self.bi_gram)

                    tri_grams = trigrams(words)
                    if not len(tri_grams) < 1:
                        for i, tri_gram in enumerate(tri_grams):
                            self.tri_gram = ' '.join(tri_gram)
                            self.statement_loc_vec = self.statement_loc_vec.replace('][', ' ')
                            self.statement_loc_vec = self.statement_loc_vec.replace('[', '')
                            self.statement_loc_vec = self.statement_loc_vec.replace(']', '')
                            self.tri_gram_index = self.statement_loc_vec + ' ' + str(
                                i) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + self.statement_loc_vec + ' ' + str(i + 2)
                            WordTagger.wordMatcherTrigram(self, self.tri_gram)

            else:
                for subtree in range(0, len(branch)):
                    WordTagger.generateLocationVector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))

    def wordMatcher(self):
        WordTagger.tf(self)
        WordTagger.idf(self)
        WordTagger.tf_idf(self)
        WordTagger.englishDictMatch(self)
        WordTagger.numberMatch(self)
        WordTagger.abbreviationMatch(self)
        WordTagger.symbolMatch(self)
        WordTagger.repetitiveWords(self)
        WordTagger.posTaggingUnigrams(self)
        WordTagger.wordSignatureWeight(self)
        WordTagger.potentialCandidates(self)

    def wordMatcherBigram(self, bi_gram):
        WordTagger.tf_bigram(self)
        WordTagger.idf_bigram(self)
        WordTagger.tf_idf_bigram(self)
        WordTagger.firstLetterOfEveryWordCapitalized(self, bi_gram)
        WordTagger.posTagging(self, bi_gram)

    def wordMatcherTrigram(self, tri_gram):
        WordTagger.tf_trigram(self)
        WordTagger.idf_trigram(self)
        WordTagger.tf_idf_trigram(self)
        WordTagger.firstLetterOfEveryWordCapitalized(self, tri_gram)
        WordTagger.posTagging(self, tri_gram)

    def tf(self):
        word_count = self.ques_words.count(self.ques_word)
        self.tf = word_count / float(len(self.ques_words))

    def tf_bigram(self):
        bigram_count = self.bi_grams.count(self.bi_gram)
        self.tf_bigram = bigram_count / float(len(self.bi_grams))

    def tf_trigram(self):
        trigram_count = self.tri_grams.count(self.tri_gram)
        self.tf_trigram = trigram_count / float(len(self.tri_grams))

    def idf(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.ques_word_count_list)):
            end += self.ques_word_count_list[i]
            if self.ques_word in self.corpus[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf = log10(float(self.ques_count + 1) / (word_occurrence + 1))

    def idf_bigram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.ques_bi_gram_count_list)):
            end += self.ques_bi_gram_count_list[i]
            if self.bi_gram in self.corpus_bigrams[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf_bigram = log10(float(self.ques_count + 1) / (word_occurrence + 1))

    def idf_trigram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.ques_tri_gram_count_list)):
            end += self.ques_tri_gram_count_list[i]
            if self.tri_gram in self.corpus_trigrams[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf_trigram = log10(float(self.ques_count + 1) / (word_occurrence + 1))

    def tf_idf(self):
        self.tf_idf = self.tf * self.idf
        # clever way to create dict with dup keys is to make values the keys | values here is a list of info
        self.signature_map = ' '.join(str(sig) for sig in self.signature_map)
        #print self.word_location_index
        self.tf_idf_list[self.tf_idf, self.word_location_index, self.signature_map] = self.ques_word

    def tf_idf_bigram(self):
        self.tfidf_bigram = self.tf_bigram * self.idf_bigram
        self.tf_idf_bigram_list[self.tfidf_bigram, self.bi_gram_index, self.signature_map] = self.bi_gram
        #print self.bi_gram, self.bi_gram_index, self.signature_map

    def tf_idf_trigram(self):
        self.tfidf_trigram = self.tf_trigram * self.idf_trigram
        self.tf_idf_trigram_list[self.tfidf_trigram, self.tri_gram_index, self.signature_map] = self.tri_gram
        #print self.tri_gram, self.tri_gram_index, self.signature_map

    def englishDictMatch(self):
        """
            matching spec word to English dictionaries
        """
        self.spell_checker_US = enchant.Dict('en_US')
        self.spell_checker_GB = enchant.Dict('en_GB')
        self.spell_checker_AU = enchant.Dict('en_AU')

        if self.ques_word_lower_case in (corpus.stopwords.words('english')):
            self.ques_english_dict_match = 'Yes (NTLK Stopword)'
            self.ques_english_dict_match_count += 1

        elif self.spell_checker_US.check(self.ques_word_lower_case) is True and not self.spell_checker_GB.check(
                self.ques_word_lower_case) is True and not self.spell_checker_AU.check(
                self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_US)'
            self.ques_english_dict_match_count += 1

        elif self.spell_checker_GB.check(self.ques_word_lower_case) is True and not self.spell_checker_US.check(
                self.ques_word_lower_case) is True and not self.spell_checker_AU.check(
                self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_GB)'
            self.ques_english_dict_match_count += 1

        elif self.spell_checker_AU.check(self.ques_word_lower_case) is True and not self.spell_checker_US.check(
                self.ques_word_lower_case) is True and not self.spell_checker_GB.check(
                self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_AU)'
            self.ques_english_dict_match_count += 1

        elif self.spell_checker_US.check(self.ques_word_lower_case) is True and self.spell_checker_GB.check(
                self.ques_word_lower_case) is True and not self.spell_checker_AU.check(
                self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_US, en_GB)'

        elif self.spell_checker_US.check(self.ques_word_lower_case) is True and self.spell_checker_AU.check(
                self.ques_word_lower_case) is True and not self.spell_checker_GB.check(
                self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_US, en_AU)'

        elif self.spell_checker_GB.check(self.ques_word_lower_case) is True and self.spell_checker_AU.check(
                self.ques_word_lower_case) is True and not self.spell_checker_US.check(
                self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_GB, en_AU)'

        elif self.spell_checker_US.check(self.ques_word_lower_case) is True and self.spell_checker_GB.check(
                self.ques_word_lower_case) is True and self.spell_checker_US.check(self.ques_word_lower_case) is True:
            self.ques_english_dict_match = 'Yes (en_US, en_GB, en_AU)'

        else:
            self.ques_english_dict_match = 'No'

    def numberMatch(self):
        if HelperFunctions.isNumber(self, self.ques_word):
            self.number_match = 'Yes'
            self.number_match_count += 1

        else:
            self.number_match = 'No'

    def abbreviationMatch(self):
        if HelperFunctions.allLowerCase(self, self.ques_word) is None and self.spell_checker_US.check(
                self.ques_word) is False:
            self.abbreviation_match = 'Yes'
            self.abbreviation_match_count += 1

        else:
            self.abbreviation_match = 'No'

    def symbolMatch(self):
        if '_' in self.ques_word or '/' in self.ques_word:
            self.symbol_match = 'Yes'
            self.symbol_match_count += 1
        else:
            self.symbol_match = 'No'

    def repetitiveWords(self):
        if self.idf == 0.0:
            self.repetitive_word = 'Yes'
            self.repetitive_word_count += 1
        else:
            self.repetitive_word = 'No'

    def posTaggingUnigrams(self):
        self.pos = pos_tag([self.ques_word])
        # NN or NNP --> Nouns (Priority Level = 1)
        if not self.ques_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                (self.pos[0][1] == 'NN' or self.pos[0][1] == 'NNP'):
            self.nouns_unigrams[self.ques_word] = self.tf_idf
        if not self.ques_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                        self.pos[0][1] == 'VB':
            self.verbs_unigrams[self.ques_word] = self.tf_idf
        if not self.ques_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0:
            if re.search(r'\b[A-Z]+(?:\W*[A-Z]+)*\b', self.ques_word):
                self.all_caps_unigrams[self.ques_word] = self.tf_idf
            if re.search(r'^[0-9]', self.ques_word):
                self.numbers_unigrams[self.ques_word] = self.tf_idf

    def wordSignatureWeight(self):
        """
            Creating words bags for Location Attributes
        """
        self.potential_tags = ['code', 'p', 'pre', 'em', 'blockquote', 'ol', 'li', 'a']
        if set(self.potential_tags) & set(self.signature_map.split()):
            self.potential_tags_found = list(set(self.potential_tags) & set(self.signature_map.split()))
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'code' in self.potential_tags_found:
                self.loc_sig_code_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'p' in self.potential_tags_found:
                self.loc_sig_p_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'pre' in self.potential_tags_found:
                self.loc_sig_pre_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'em' in self.potential_tags_found:
                self.loc_sig_em_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words(
                        'english')) and not self.idf == 1.0 and 'blockquote' in self.potential_tags_found:
                self.loc_sig_blockquote_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'ol' in self.potential_tags_found:
                self.loc_sig_ol_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'li' in self.potential_tags_found:
                self.loc_sig_li_unigrams[self.ques_word] = self.tf_idf
            if not self.ques_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'a' in self.potential_tags_found:
                self.loc_sig_a_unigrams[self.ques_word] = self.tf_idf

    def firstLetterOfEveryWordCapitalized(self, string):
        cap_count = 0
        words = string.split()
        for word in words:
            if word[0].isupper():
                cap_count += 1
        if cap_count == len(words):
            self.first_letter_cap = "Yes"
        else:
            self.first_letter_cap = "No"

    def posTagging(self, string):
        """
        POS Tagger for bigrams | trigrams
        """
        #words = word_tokenize(string)
        words = string.split()
        self.pos = pos_tag(words)
        self.pos = [x[1] for x in self.pos]

        # POS word bags for bigrams
        if len(self.pos) == 2 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP':
            self.bigram_NNP_NNP[string] = self.tfidf_bigram

        if len(self.pos) == 2 and self.pos[0] == 'NNP' and self.pos[1] == 'NN':
            self.bigram_NNP_NN[string] = self.tfidf_bigram

        if len(self.pos) == 2 and self.pos[0] == 'NN' and self.pos[1] == 'NN':
            self.bigram_NN_NN[string] = self.tfidf_bigram

        if len(self.pos) == 2 and self.pos[0] == 'NN' and self.pos[1] == 'NNS':
            self.bigram_NN_NNS[string] = self.tfidf_bigram

        if len(self.pos) == 2 and self.pos[0] == 'NN' and self.pos[1] == 'VBD':
            self.bigram_NN_VBD[string] = self.tfidf_bigram

        # POS word bags for trigrams
        if len(self.pos) == 3 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP' and self.pos[2] == 'NNP':
            self.trigram_NNP_NNP_NNP[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP' and self.pos[2] == 'NN':
            self.trigram_NNP_NNP_NN[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NNP' and self.pos[1] == 'NN' and self.pos[2] == 'NN':
            self.trigram_NNP_NN_NN[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NN' and self.pos[1] == 'NN' and self.pos[2] == 'NN':
            self.trigram_NN_NN_NN[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NN' and self.pos[1] == 'NN' and self.pos[2] == 'CD':
            self.trigram_NN_NN_CD[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NN' and self.pos[1] == 'NNS' and self.pos[2] == 'CD':
            self.trigram_NN_NNS_CD[string] = self.tfidf_trigram

    def potentialCandidates(self):
        # common English dictionary words
        if not self.ques_word_lower_case in (
            corpus.stopwords.words('english')) and not self.idf == 1.0 and self.spell_checker_US.check(
                self.ques_word_lower_case) is True:
            self.common_eng_words[self.ques_word] = self.tf_idf

        # common English words that are all upper case
        if not self.ques_word_lower_case in (
            corpus.stopwords.words('english')) and not self.idf == 1.0 and self.spell_checker_US.check(
                self.ques_word_lower_case) is True and HelperFunctions.allLowerCase(self, self.ques_word) is None:
            self.common_eng_words_UPPER[self.ques_word] = self.tf_idf

        # ABBREVIATION cluster
        if not self.ques_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                        self.abbreviation_match == 'yes':
            self.abbreviation_cluster[self.ques_word] = self.tf_idf