class Graph:

    def __init__(self, genes, repeats, classifications, array3D, threshold=1):
        self.gene_obj = []
        self.threshold = int(threshold)
        self.genes = genes
        self.repeats = repeats
        self.classifications = classifications
        self.array3D = array3D

    def add_node(self, node):
        """ add node to gene_obj list """
        self.gene_obj.append(node)

    def compareAll(self):
        """ call compare() on all nodes comparing to every other nodes """
        # iterate through list of gene nodes by index
        size = len(self.gene_obj)
        for curr_gene in range(size):
            if curr_gene % 500 == 0:
                print("Compared {} genes".format(curr_gene))
            # find the gene at index i
            for compare_gene in range(curr_gene, size):
                self.compare(curr_gene, compare_gene)

    def compare(self, curr_gene, compare_gene):
        """ compare node to every other node"""
        for TE in range(len(self.repeats)):
            for classification in range(len(self.classifications)):
                # create edge between gene A and gene B if they both pass threshold
                if self.array3D[curr_gene][TE][classification] >= self.threshold and \
                        self.array3D[compare_gene][TE][classification] >= self.threshold:
                    self.gene_obj[curr_gene].neighbors.add(compare_gene)
                    self.gene_obj[compare_gene].neighbors.add(curr_gene)

    def disjointSet(self):
        # create instance of disjoint set class
        self.disjoint = disjointSets(self.gene_obj)

        # iterate over indexes of genes
        for gene in range(len(self.gene_obj)):
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

    def print(self, fileName):
        """ write output to txt file """
        graphiTE_file = open(fileName, 'w')
        for parent in range(len(self.subsets)):
            neighborhood = self.subsets[parent]
            graphiTE_file.write("{} \t {} \t {} \n".format(parent, neighborhood, len(neighborhood)))

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