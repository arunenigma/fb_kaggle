# -*- coding: utf-8 -*-

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from master_table import *
from model import *
from prioritize import *
from read_train import *

if __name__ == '__main__':
    hd5_file = pandas.HDFStore('Train.h5', 'w')
    csv_file = read_csv('Train.csv', iterator=True, chunksize=100)
    p = Prioritize()
    # master <--> train
    train_PI_bundles = p.prioritizeDataTRAIN(hd5_file, csv_file)
    master = MasterTable()
    master_table = master.unRavelMasterBundle(train_PI_bundles)

    hd5_file = pandas.HDFStore('Test.h5', 'w')
    csv_file = read_csv('Test.csv', iterator=True, chunksize=10)
    test_PI_bundles = p.prioritizeDataTEST(hd5_file, csv_file)

    model = FuzzyModel()
    model.unRavelTestPIBundle(test_PI_bundles, master_table)
