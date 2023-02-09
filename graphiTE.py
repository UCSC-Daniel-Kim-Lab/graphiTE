class Node:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.parent = name

    def __repr__(self):
        return f"{self.name} Size {self.size}"

def union_by_size(node1, node2):
    root1 = find(node1)
    root2 = find(node2)

    if root1 != root2:
        # update parent node to gene with most connections
        if root1.size < root2.size:
            root1.parent = root2
        else:
            root2.parent = root1

def find(node):
    if node.parent == node.name:
        return node
    node.parent = find(node.parent)

    return node.parent

def main():
    file = open('graphite_data.csv')
    file.readline()

    # initialize adjacency list and mapping dictionary
    adj_list = {}
    gene_map = {}

    count = 0

    for lines in file.readlines():

        # change sample size here
        if count == 95000:
            break

        # parse csv
        line = lines.split(',')

        gene_name = line[0]
        repeat = line[3]

        # map new gene to new gene object
        # (otherwise, will create new object for every instance of gene)
        if gene_name not in gene_map:
            gene = Node(gene_name)
            gene_map[gene_name] = gene

        # get gene object
        gene = gene_map[gene_name]

        # create adjacency list
        if repeat not in adj_list:
            adj_list[repeat] = set()

        adj_list[repeat].add(gene)

        # count connections
        gene.size += 1

        count += 1

    # union all nodes with the same repeat
    for nodes in adj_list.values():
        nodes = list(nodes)
        for i in range(1, len(nodes)):
            union_by_size(nodes[i], nodes[i - 1])

    # print the final parent of each node
    for gene in gene_map.values():
        if gene.name == find(gene).name:
            print(f"{gene.name} is the parent")

main()
