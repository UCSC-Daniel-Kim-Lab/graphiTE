import pandas as pd
import numpy as np

# load csv file in df
data = pd.read_csv('/Users/queenie1/Desktop/kimlab/data/graphiTE_shuf100_test.csv')

# get gene, repeat, and classification
genes = data['name2'].unique()
repeats = data['repName'].unique()
classifications = data['classification'].unique()

# create 3D numpy array initialized with zeros
array_3d = np.zeros((len(genes), len(repeats), len(classifications)), dtype=int)

# loop through the rows of the data and fill the array with number of matches
for index, row in data.iterrows():
    gene_index = np.where(genes == row['name2'])[0][0]
    repeat_index = np.where(repeats == row['repName'])[0][0]
    classification_index = np.where(classifications == row['classification'])[0][0]
    array_3d[gene_index, repeat_index, classification_index] += 1


class Graph:

    def __init__(self):
        self.gene_obj = []

    def add_node(self, node):
        """ add node to gene_obj list """
        self.gene_obj.append(node)

    def compareAll(self):
        """ call compare() on all nodes comparing to every other nodes """
        # iterate through list of gene nodes by index
        for i in range(len(self.gene_obj)):
            # find the gene at index i
            gene = self.gene_obj[i]
            # update gene's neighbors with new neighbors from compare()
            gene.neighbors.update(self.compare(gene.gene_name))

    def compare(self, gene):
        """ compare node to every other node, skipping nodes that have been compared """

        # get position of gene
        gene_pos = np.where(genes == gene)[0][0]

        # initialize empty set to store neighbors
        neighbors = set()

        # loop by columns, rows
        for TE in range(len(repeats)):
            for gene_row in range(len(genes)):
                # check if current rows neighbor contains the gene we're looking at
                if gene_pos in self.gene_obj[gene_row].neighbors:
                    continue
                for classification in range(len(classifications)):
                    # make sure we only do meaningful comparisons
                    if gene_pos == gene_row or array_3d[gene_pos][TE][classification] == 0:
                        continue
                    # add index to neighbors set
                    if array_3d[gene_row][TE][classification] > 0:
                        neighbors.add(gene_row)
                        # if A in B, add A to B neighbors
                        self.gene_obj[gene_row].neighbors.add(gene_pos)

        return neighbors


class Gene:

    def __init__(self, gene_name):
        self.gene_name = gene_name

        self.neighbors = set()

    def __repr__(self):
        return f"{self.gene_name, self.neighbors}"


def main():
    graph = Graph()

    # create gene nodes for each gene and add to Graph object
    for gene_index in range(len(genes)):
        node = Gene(genes[gene_index])
        graph.add_node(node)

    # compare nodes
    graph.compareAll()

    # print
    for gene in range(len(graph.gene_obj)):
        if len(graph.gene_obj[gene].neighbors) > 0:
            print('{} {}'.format(gene, graph.gene_obj[gene]))

main()









