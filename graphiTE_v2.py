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

    def disjointSet(self):
        # create instance of disjoint set class
        self.disjoint = disjointSets(self.gene_obj)

        # iterate over indexes of genes
        for gene in range(len(self.gene_obj)):
            # print
            # if len(self.gene_obj[gene].neighbors) > 0:
                # print('{} {}'.format(gene, self.gene_obj[gene]))
            # call union_find on gene index, and neighbor indexes
            for neighbor in self.gene_obj[gene].neighbors:
                self.disjoint.union(gene, neighbor)

    def createParentSets(self):
        # [roots] rep all gene_obj
        # node @ graph.gene_obj[0] has parent at index roots[0]
        self.subsets = [set() for _ in range(len(self.gene_obj))]

        # add all children of a parent node to the subset list @ the parent nodes index
        for i in range(len(self.disjoint.roots)):
            self.subsets[self.disjoint.roots[i]].add(i)

        # filter out any empty sets or nodes where the subset is 1
        # print(list(filter(lambda x: len(x) > 0, self.subsets)))

    def store_trees(self):
        self.trees = [(self.disjoint.roots[i], self.disjoint.ranks[i]) for i in range(len(self.gene_obj))]

    def print(self, fileName):
        file = open(fileName, 'w')
        for parent in range(len(self.subsets)):
            neighborhood = self.subsets[parent]
            if len(neighborhood) > 0:
                children = neighborhood.copy()
                children.remove(parent)
                file.write("{} | {} | {} \n".format(parent, children, len(neighborhood)))

class Gene:

    def __init__(self, gene_name):
        self.gene_name = gene_name

        self.root = self

        self.neighbors = set()

    def __repr__(self):
        return f"{self.gene_name, self.neighbors}"


class disjointSets:

    def __init__(self, gene_obj):
        # initialize all roots as its own subset
        self.roots = [node for node in range(len(gene_obj))]
        # set all ranks to 1
        self.ranks = [1 for _ in range(len(gene_obj))]

    def find(self, node):
        # find parent root
        if node != self.roots[node]:
            self.roots[node] = self.find(self.roots[node])
            return self.roots[node]
        return node

    def union(self, left_index, right_index):
        # union by rank optimization
        root_left = self.find(left_index)
        root_right = self.find(right_index)

        # union left root and right root based off rank
        if root_left == root_right:
            return True
        if self.ranks[root_left] > self.ranks[root_right]:
            self.roots[root_right] = root_left
        elif self.ranks[root_right] > self.ranks[root_left]:
            self.roots[root_left] = root_right
        else:
            self.roots[root_left] = root_right
            self.ranks[root_right] += 1
        return False


def main():
    graph = Graph()

    # create gene nodes for each gene and add to Graph object
    for gene_index in range(len(genes)):
        node = Gene(genes[gene_index])
        graph.add_node(node)

    # compare nodes
    graph.compareAll()

    graph.disjointSet()
    graph.createParentSets()
    graph.print("test.txt")
    # print()
    graph.store_trees()
    # print(graph.trees)


main()










