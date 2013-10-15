from read import *
from parse_title import *

if __name__ == '__main__':
    hd5_file = pandas.HDFStore('Train.h5', 'w')
    csv_file = read_csv('Train.csv', iterator=True, chunksize=1000)
    read = ReadData()
    read.chunkAndDataStreamData(hd5_file, csv_file)
    ids = read.ids
    titles = read.titles
    bodies = read.bodies
    tags = read.tags
    parse_title = ParseTitle(titles)
    parse_title.parseTitle()

