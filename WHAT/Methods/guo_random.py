from __future__ import division
from random import shuffle, choice
from Utilities.performance_measure import *
from Utilities.model import generate_model


class guo_random:
    def __init__(self, filename):
        self.filename = filename
        self.temp_file_name = "temp_file.csv"

    def temp_file_generation(self, header, listoflist):
        import csv
        with open(self.temp_file_name, 'wb') as fwrite:
            writer = csv.writer(fwrite, delimiter=',')
            writer.writerow(header)
            for l in listoflist:
                writer.writerow(l)
        fwrite.close()

    def where_clusterer(self):
        """
        This is function accepts a file with rows(=records) and clusters it. This is FASTNAP + PCA
        :param filename: Pass in the filename with rows as valid configurations
        :return: List of Cluster. Each cluster has a [[cluster_number], [list of members]]
        """
        from Utilities.Tools.methods1 import wrapper_createTbl
        # The Data has to be access using this attribute table._rows.cells
        transformed_table = [[int(z) for z in x.cells[:-1]] + x.cells[-1:] for x in wrapper_createTbl(self.temp_file_name)._rows]
        cluster_numbers = set(map(lambda x: x[-1], transformed_table))

        # separating clusters
        # the element looks like [clusterno, rows]
        cluster_table = []
        for number in cluster_numbers:
            cluster_table.append([number] + [filter(lambda x: x[-1] == number, transformed_table)])
        return cluster_table

    def generate_test_data(self, number):
        raw_content = open(self.filename, "r").readlines()
        header = raw_content[0].split(",")
        content = [map(float, rc.split(",")) for rc in raw_content[1:]]
        indexes = range(len(content))
        shuffle(indexes)

        breakpoint = int(0.4 * len(content))

        train_indexes = indexes[:breakpoint]
        test_indexes = indexes[breakpoint:]

        train_independent = []
        train_dependent = []

        test_independent = []
        test_dependent = []

        for ti in train_indexes:
            train_independent.append(map(float, content[ti][:-1]))
            train_dependent.append(float(content[ti][-1]))

        assert (len(train_independent) == len(train_dependent)), "something wrong"

        for ti in test_indexes:
            test_independent.append(map(float, content[ti][:-1]))
            test_dependent.append(float(content[ti][-1]))

        assert (len(test_independent) == len(test_dependent)), "something wrong"

        train_indexes = range(len(train_independent))
        shuffle(train_indexes)

        selected_points_indep = [train_independent[i] for i in xrange(len(train_indexes[:number]))]
        selected_points_dep = [train_dependent[i] for i in xrange(len(train_indexes[:number]))]
        return [selected_points_indep, selected_points_dep], [test_independent, test_dependent]



if __name__ == "__main__":
    mmre = []
    for _ in xrange(30):
        method = guo_random("./Data/Apache_AllMeasurements.csv")
        training_data, testing_data = method.generate_test_data()
        assert(len(training_data[0]) == len(training_data[-1])), "Something is wrong"
        assert(len(testing_data[0]) == len(testing_data[-1])), "Something is wrong"
        mmre.append(generate_model(training_data, testing_data))

    print np.median(mmre)