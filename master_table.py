class MasterTable(object):
    def __init__(self):
        self.master_table = []

    def unRavelMasterBundle(self, master_bundles):
        for master_bundle in master_bundles:
            for ID, prioritized_keywords in master_bundle.iteritems():
                for keyword, PI in prioritized_keywords.iteritems():
                    if len(PI) > 1:
                        if PI[0] > 0.5:
                            print ID, keyword, PI[0], 1
                    else:
                        if PI[0] > 0.5:
                            print ID, keyword, PI[0], 0