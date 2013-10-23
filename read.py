__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2013, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from pandas import *
import tables


class ReadData(object):
    def __init__(self):
        self.ids = []
        self.titles = []
        self.bodies = []
        self.tags = []

    def chunkAndDataStreamData(self, hd5_file, csv_file, dataset_type):
        id_chunks = []
        title_chunks = []
        body_chunks = []
        tags_chunks = []

        for i, chunk in enumerate(csv_file):
            if not i > 1:
                id_chunks.append(chunk['Id'])
                title_chunks.append(chunk['Title'])
                body_chunks.append(chunk['Body'])
                if not dataset_type is 'Test':
                    tags_chunks.append(chunk['Tags'])
                else:
                    pass
            else:
                break

        id_chunks_cc = concat(id_chunks, ignore_index=True)
        title_chunks_cc = concat(title_chunks, ignore_index=True)
        body_chunks_cc = concat(body_chunks, ignore_index=True)
        if not dataset_type is 'Test':
            self.tags_chunks_cc = concat(tags_chunks, ignore_index=True)
        else:
            pass

        df_id = DataFrame()
        df_title = DataFrame()
        df_body = DataFrame()
        if not dataset_type is 'Test':
            self.df_tags = DataFrame()
        else:
            pass

        df_id_data = DataFrame(id_chunks_cc)
        df_id = df_id.append(df_id_data, ignore_index=True)
        df_title_data = DataFrame(title_chunks_cc)
        df_title = df_title.append(df_title_data, ignore_index=True)
        df_body_data = DataFrame(body_chunks_cc)
        df_body = df_body.append(df_body_data, ignore_index=True)

        if not dataset_type is 'Test':
            df_tags_data = DataFrame(self.tags_chunks_cc)
            self.df_tags = self.df_tags.append(df_tags_data, ignore_index=True)
        else:
            pass

        hd5_file['Id'] = df_id
        hd5_file['Title'] = df_title
        hd5_file['Body'] = df_body

        if not dataset_type is 'Test':
            hd5_file['Tags'] = self.df_tags
        else:
            pass

        hd5_file.close()

        if not dataset_type is 'Test':
            hd5_file = tables.openFile("Train.h5", driver="H5FD_CORE")
        else:
            hd5_file = tables.openFile("Test.h5", driver="H5FD_CORE")

        for group in hd5_file.walk_groups("/Id"):
            for array in hd5_file.list_nodes(group, classname='Array'):
                if 'axis1' in str(array):
                    self.ids = list(array)

        for group in hd5_file.walk_groups("/Title"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                self.titles = list(array)[0]

        for group in hd5_file.walk_groups("/Body"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                self.bodies = list(array)[0]

        if not dataset_type is 'Test':
            for group in hd5_file.walk_groups("/Tags"):
                for array in hd5_file.list_nodes(group, classname='VLArray'):
                    if 'block0' in str(array):
                        self.tags = list(array)[0]
        else:
            pass

        hd5_file.close()