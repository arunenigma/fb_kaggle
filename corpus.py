# -*- coding: utf-8 -*-
from io import BytesIO

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from nltk import bigrams, trigrams
from string import maketrans
from lxml import etree


class Corpus(object):
    def __init__(self, body, spec_words, bi_grams, tri_grams):
        self.body = body
        self.spec_words = spec_words
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
                        symbols = ",[]();:<>+=&+%!@#~?{}|\""
                        whitespace = "                       "
                        replace = maketrans(symbols, whitespace)
                        spec_word = word_location[1].translate(replace)
                        spec_word = spec_word.lstrip()
                        spec_word = spec_word.rstrip()

                        if len(spec_word) > 1 and not len(spec_word) > 16:
                            self.spec_words.append(spec_word)

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
                    Corpus.generateLocationVector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))