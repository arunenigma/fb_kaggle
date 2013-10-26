# -*- coding: utf-8 -*-

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from pandas import *
import tables


class ReadDataTEST(object):
    def __init__(self):
        self.ids_test_holder = []
        self.ids_test = []
        self.titles_test = []
        self.bodies_test = []

    def chunkAndDataStreamDataTEST(self, hd5_file, csv_file):
        id_chunks = []
        title_chunks = []
        body_chunks = []

        for i, chunk in enumerate(csv_file):
            if not i > 1:  # tap for input data
                id_chunks.append(chunk['Id'])
                title_chunks.append(chunk['Title'])
                body_chunks.append(chunk['Body'])
            else:
                break

        id_chunks_cc = concat(id_chunks, ignore_index=True)
        title_chunks_cc = concat(title_chunks, ignore_index=True)
        body_chunks_cc = concat(body_chunks, ignore_index=True)

        df_id = DataFrame()
        df_title = DataFrame()
        df_body = DataFrame()

        df_id_data = DataFrame(id_chunks_cc)
        df_id = df_id.append(df_id_data, ignore_index=True)
        df_title_data = DataFrame(title_chunks_cc)
        df_title = df_title.append(df_title_data, ignore_index=True)
        df_body_data = DataFrame(body_chunks_cc)
        df_body = df_body.append(df_body_data, ignore_index=True)

        hd5_file['Id'] = df_id
        hd5_file['Title'] = df_title
        hd5_file['Body'] = df_body

        hd5_file.close()

        hd5_file = tables.openFile("Test.h5", driver="H5FD_CORE")

        for group in hd5_file.walk_groups("/Id"):
            for array in hd5_file.list_nodes(group, classname='Array'):
                self.ids_test_holder = list(array)

        for ID in self.ids_test_holder:
            self.ids_test.append(ID[0])

        for group in hd5_file.walk_groups("/Title"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                self.titles_test = list(array)[0]

        for group in hd5_file.walk_groups("/Body"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                self.bodies_test = list(array)[0]

        hd5_file.close()