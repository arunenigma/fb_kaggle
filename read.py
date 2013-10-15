from pandas import *
import tables


class ReadData(object):
    def chunkAndDataStreamData(self, hd5_file, csv_file):
        id_chunks = []
        title_chunks = []
        body_chunks = []
        tags_chunks = []

        for i, chunk in enumerate(csv_file):
            if not i > 100:
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
                if 'axis1' in str(array):
                    print list(array)

        for group in hd5_file.walk_groups("/Title"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                print list(array)[0]

        for group in hd5_file.walk_groups("/Body"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                print list(array)[0]

        for group in hd5_file.walk_groups("/Tags"):
            for array in hd5_file.list_nodes(group, classname='VLArray'):
                if 'block0' in str(array):
                    print list(array)[0]
