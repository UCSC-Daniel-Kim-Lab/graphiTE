import pandas as pd
import numpy as np

# load csv file in df
data = pd.read_csv('/Users/queenie1/Desktop/kimlab/data/graphiTE_shuf100_test.csv')

# get rid of duplicates
genes = data['name2'].unique()
repeats = data['repName'].unique()
classifications = data['classification'].unique()

# create 3D numpy array initialized with zeros
array_3d = np.zeros((len(genes), len(repeats), len(classifications)), dtype=float)

# loop through the rows of the data and fill the array with 1s where there's a match
for index, row in data.iterrows():
    gene_index = np.where(genes == row['name2'])[0][0]
    repeat_index = np.where(repeats == row['repName'])[0][0]
    classification_index = np.where(classifications == row['classification'])[0][0]
    array_3d[gene_index, repeat_index, classification_index] = 1

def compare(gene):

    # get position of gene
    gene_pos = np.where(genes == gene)[0][0]

    # initialize empty set to store neighbors
    neighbors = set()

    # loop by columns, rows
    for TE in range(len(repeats)):
        for gene_row in range(len(genes)):
            for classification in range(len(classifications)):
                # make sure we only do meaningful comparisons
                if gene_pos == gene_row or array_3d[gene_pos][TE][classification] == 0:
                    continue
                # add index to neighbors set
                if array_3d[gene_row][TE][classification] == 1:
                    neighbors.add(gene_row)

    return neighbors

class Graph:
    gene_obj = genes

class Gene:

    def __init__(self, gene_name):
        self.gene_name = gene_name

        self.neighbors = compare(self.gene_name)

    def __repr__(self):
        return f"{self.gene_name}"

def main():
    graph = Graph()

    for gene_index in range(len(graph.gene_obj)):
        node = Gene(graph.gene_obj[gene_index])
        if len(node.neighbors) > 0:
            print('{} {} {}'.format(gene_index, node.gene_name, node.neighbors))

main()




