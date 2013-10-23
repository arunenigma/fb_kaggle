import numpy as np
import csv
import sys


class VectorSpaceModel(object):
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
        self.doc_A = {}
        self.doc_B = {}
        self.doc_vec_A = []
        self.doc_vec_B = []

    def readCsvFiles(self):
        self.f1.next()
        self.f2.next()
        for row in self.f1:
            self.doc_A[row[0]] = float(row[1])
        for row in self.f2:
            self.doc_B[row[0]] = float(row[1])
        for word, pi_score_A in self.doc_A.iteritems():
            try:
                pi_score_B = self.doc_B[word]
                self.doc_vec_A.append(float(pi_score_A))
                self.doc_vec_B.append(float(pi_score_B))

            except KeyError:
                self.doc_vec_A.append(float(pi_score_A))
                self.doc_vec_B.append(0.0)

    def cosSimilarity(self):
        num = np.dot(self.doc_vec_A, self.doc_vec_B)
        denum = (np.sqrt(np.dot(self.doc_vec_A, self.doc_vec_A)) * np.sqrt(np.dot(self.doc_vec_B, self.doc_vec_B)))
        cos_sim = num / denum
        print cos_sim

if __name__ == '__main__':
    f1 = csv.reader(open(sys.argv[1], 'rb'))
    f2 = csv.reader(open(sys.argv[2], 'rb'))
    v = VectorSpaceModel(f1, f2)
    v.readCsvFiles()
    v.cosSimilarity()