import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--csv_file')
parser.add_argument('-t', '--threshold', default=1)
parser.add_argument('-o', '--output_file')
parser.add_argument('-p', '--prints', default=250)

args = parser.parse_args()

csvFile = args.csv_file
threshold = int(args.threshold)
outFile = args.output_file
verbosity = int(args.prints)

# load csv file in df
data = pd.read_csv(csvFile)

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

    def __init__(self, threshold=1):
        self.gene_obj = []
        self.threshold = threshold

    def add_node(self, node):
        """ add node to gene_obj list """
        self.gene_obj.append(node)

    def compareAll(self):
        """ call compare() on all nodes comparing to every other nodes """
        # iterate through list of gene nodes by index
        size = len(self.gene_obj)
        for curr_gene in range(size):
            if curr_gene % verbosity == 0:
                print("Connected {} genes".format(curr_gene))
            # find the gene at index i
            for compare_gene in range(curr_gene, size):
                self.compare(curr_gene, compare_gene)
        print("Completed Graph Generation")

    def compare(self, curr_gene, compare_gene):
        """ compare node to every other node"""
        for TE in range(len(repeats)):
            for classification in range(len(classifications)):
                # create edge between gene A and gene B if they both pass threshold
                if array_3d[curr_gene][TE][classification] >= self.threshold and \
                        array_3d[compare_gene][TE][classification] >= self.threshold:
                    self.gene_obj[curr_gene].neighbors.add(compare_gene)
                    self.gene_obj[compare_gene].neighbors.add(curr_gene)

    def disjointSet(self):
        # create instance of disjoint set class
        self.disjoint = disjointSets(self.gene_obj)

        # iterate over indexes of genes
        for gene in range(len(self.gene_obj)):
            # call union_find on gene index, and neighbor indexes
            if (gene%verbosity==0): print("Compared {} genes".format(gene))
            for neighbor in self.gene_obj[gene].neighbors:
                self.disjoint.union(gene, neighbor)
        print("Finished Finding Connections")

    def createParentSets(self):
        # [roots] rep all gene_obj
        # node @ graph.gene_obj[0] has parent at index roots[0]
        print("Formatting Output")
        parents = {parent: index for index, parent in enumerate(set(self.disjoint.roots))} # pull true roots
        print("{} Distinct Sets Found".format(len(parents.keys())))

        self.subsets = [[] for _ in parents.keys()] # def one set for each true root
        for node in range(len(self.disjoint.roots)): # add each node to the set for its root
            self.subsets[parents[self.disjoint.roots[node]]].append(node)
        self.subsets.sort(key=lambda s: len(s), reverse=True)

    def print(self, fileName):
        """ write output to txt file """
        with open(fileName, 'w') as file:
            print("\t".join([str(len(subset)) for subset in self.subsets]), file=file)
            for i in range(max([len(subset) for subset in self.subsets])):
                print("\t".join([str(subset[i]) if i < len(subset) else " " for subset in self.subsets]), file=file)

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
        while node != self.roots[node]:
            self.roots[node] = self.roots[self.roots[node]]
            node = self.roots[node]
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
    # pass threshold here
    graph = Graph()

    # create gene nodes for each gene and add to Graph object
    for gene in genes:
        graph.add_node(Gene(gene))

    # compare nodes
    graph.compareAll() # Create Graph
    graph.disjointSet() # Init Sets
    graph.createParentSets() # Find Connectivity
    graph.print(outFile) # Print Results

main()
