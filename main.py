from read import *

if __name__ == '__main__':
    hd5_file = pandas.HDFStore('Train.h5', 'w')
    csv_file = read_csv('Train.csv', iterator=True, chunksize=100)
    read = ReadData()
    read.chunkAndDataStreamData(hd5_file, csv_file)