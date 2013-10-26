# -*- coding: utf-8 -*-

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from math import fabs


class FuzzyModel(object):
    def unRavelTestPIBundle(self, test_PI_bundle, master_table):
        print '*************************************************'
        print '*             Neuro-fuzzy Brain                 *'
        print '*************************************************'

        predictions = []
        for bundle in test_PI_bundle:
            for ID, prioritized_keywords in bundle.iteritems():
                for keyword, PI in prioritized_keywords.iteritems():
                    #print ID, keyword, PI, PI[0], PI[-1]
                    for t_data in master_table:
                        if keyword == t_data[1]:
                            if not t_data[3] is None:
                                predictions.append([ID, t_data[1], 1.0 - fabs(t_data[2]-PI[0])])

        # remove duplicates
        predictions = dict((x[0], x) for x in predictions).values()
        for prediction in predictions:
            print prediction[0], prediction[1], prediction[2]