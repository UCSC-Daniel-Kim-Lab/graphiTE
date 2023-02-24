class Node:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.parent = self
        self.repeats = set()
        self.children = set()
        self.overlappedRepeats = {}

    def __repr__(self):
        # represent object as gene name and size
        return f"{self.name} Size {self.size} Children {len(self.children)}"

    def intersect(self, node):
        """
        return boolean if two nodes have intersecting repeats
        """
        return len(self.repeats.intersection(node.repeats)) > 0

    def findOverlap(self, node):
        """
        find the overlapping repeats between one node and another
        """

        if node in self.overlappedRepeats:
            return

        intersectSet = self.repeats.intersection(node.repeats)

        self.overlappedRepeats[node] = intersectSet
        node.overlappedRepeats[self] = intersectSet

def mergeNodes(node1, node2):
    """
    merge two nodes, setting the parent to be the one with the most amount of repeats
    """

    parent, child = (node1, node2) if len(node1.repeats) >= len(node2.repeats) else (node2, node1)

    # reassign child's parent
    child.parent = parent

    # add child to parent's children
    parent.children.add(child)

    # union the repeats -> parent now has the child's repeats too
    parent.repeats = parent.repeats.union(child.repeats)

    return parent


def main():
    file = open('graphite_data.csv')
    # skip header
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

        if gene_name not in gene_map:
            gene = Node(gene_name)
            gene_map[gene_name] = gene

        gene = gene_map[gene_name]
        gene.repeats.add(repeat)

        # count connections
        gene.size += 1

        count += 1

    # create a set of genes
    geneSet = set(gene_map.values())

    # pop a random gene and set as current parent
    parent = geneSet.pop()

    # variable to ensure we don't loop forever if we can't add any gene from the set
    foundIntersectCycle = True

    # while there are genes to add & we haven't done a cycle through the set where we didn't intersect any genes
    while len(geneSet) > 0 and foundIntersectCycle:
        foundIntersectCycle = False

        # create set of merged genes to remove after loop
        removeSet = set()

        # iterate through set, compare each gene to the parent gene -> if they intersect -> merge them together
        for setItem in geneSet:
            if parent.intersect(setItem):
                parent.findOverlap(setItem)
                parent = mergeNodes(parent, setItem)
                removeSet.add(setItem)

                # continue
                foundIntersectCycle = True

        # remove added genes
        geneSet = geneSet.difference(removeSet)

    print(parent)

main()
