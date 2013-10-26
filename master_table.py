class MasterTable(object):
    def __init__(self):
        self.train_data_table = []

    def unRavelMasterBundle(self, train_bundles):
        for train_bundle in train_bundles:
            for ID, prioritized_keywords in train_bundle.iteritems():
                for keyword, PI in prioritized_keywords.iteritems():
                    if len(PI) > 1:
                        if PI[0] > 0.5:
                            self.train_data_table.append([ID, keyword, PI[0], PI[1]])
                    else:
                        if PI[0] > 0.5:
                            self.train_data_table.append([ID, keyword, PI[0], None])
        return self.train_data_table