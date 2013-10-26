__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from pandas import *
import tables


class ReadDataTRAIN(object):
    def __init__(self):
        self.ids_train_holder = []
        self.ids_train = []
        self.titles_train = []
        self.bodies_train = []
        self.tags_train = []

    def chunkAndDataStreamDataTRAIN(self, hd5_file, csv_file):
        id_chunks = []
        title_chunks = []
        body_chunks = []
        tags_chunks = []

        for i, chunk in enumerate(csv_file):
            if not i > 1:  # tap for input data
                id_chunks.append(chunk['Id'])
                title_chunks.append(chunk['Title'])
                body_chunks.append(chunk['Body'])
                tags_chunks.append(chunk['Tags'])
            else:
                break

        id_chunks_cc = concat(id_chunks, ignore_index=True)
        title_chunks_cc = concat(title_chunks, ignore_index=True)
        body_chunks_cc = concat(body_chunks, ignore_index=True)
        tags_chunks_cc = concat(tags_chunks, ignore_index=True)

        df_id = DataFrame()
        df_title = DataFrame()
        df_body = DataFrame()
        df_tags = DataFrame()

        df_id_data = DataFrame(id_chunks_cc)
        df_id = df_id.append(df_id_data, ignore_index=True)
        df_title_data = DataFrame(title_chunks_cc)
        df_title = df_title.append(df_title_data, ignore_index=True)
        df_body_data = DataFrame(body_chunks_cc)
        df_body = df_body.append(df_body_data, ignore_index=True)
        df_tags_data = DataFrame(tags_chunks_cc)
        df_tags = df_tags.append(df_tags_data, ignore_index=True)

        hd5_file['Id'] = df_id
        hd5_file['Title'] = df_title
        hd5_file['Body'] = df_body
        hd5_file['Tags'] = df_tags

        hd5_file.close()

        hd5_file = tables.openFile("Train.h5", driver="H5FD_CORE")

        for group in hd5_file.walk_groups("/Id"):
            for array in hd5_file.list_nodes(group, classname='Array'):
                self.ids_train_holder = list(array)

        for ID in self.ids_train_holder:
            self.ids_train.append(ID[0])

        for group in hd5_file.walk_groups("/Title"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                self.titles_train = list(array)[0]

        for group in hd5_file.walk_groups("/Body"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                self.bodies_train = list(array)[0]

        for group in hd5_file.walk_groups("/Tags"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                if 'block0' in str(array):
                    self.tags_train = list(array)[0]

        hd5_file.close()