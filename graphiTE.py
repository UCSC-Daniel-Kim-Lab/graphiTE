class Node:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.parent = self
        self.repeats = set()
        self.children = set()
        self.overlappedRepeats = {}
        self.maxDepth = 0

    def __repr__(self):
        # represent object as gene name
        return f"{self.name}"

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

        self.overlappedRepeats[node] = intersectSet             # for node1 ->  new gene2 : intersecting repeats
        node.overlappedRepeats[self] = intersectSet             # for node2 -> new gene1 : intersecting repeats

def findParent(node1, node2):
    """
    merge two nodes, setting the parent to be the one with the most amount of repeats
    """
    # edge case
    if node1 == node2:
        return node1

    # set parent and child based on number of repeats
    parent, child = (node1, node2) if len(node1.repeats) >= len(node2.repeats) else (node2, node1)

    # reassign child's parent
    child.parent = parent

    # which has the greatest path? (level of descendants)
    parent.maxDepth = max(parent.maxDepth, child.maxDepth + 1)

    # add child to parent's children
    parent.children.add(child)

    return parent

def main():
    file = open('filt_data.csv')
    # skip header
    file.readline()

    # initialize adjacency list and mapping dictionary
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
    geneList = set(gene_map.values())

    # start at gene with the least amount of repeats
    geneList = sorted(geneList, key=lambda x: len(x.repeats))

    # make parent first gene in list ^
    parent = geneList[0]

    # variable to ensure we don't loop forever if we can't add any gene from the set
    foundIntersectCycle = True

    # while there are genes to add & we haven't done a cycle through the set where we didn't intersect any genes
    while len(geneList) > 0 and foundIntersectCycle:
        foundIntersectCycle = False

        # create set of merged genes to remove after loop
        removeList = []

        # iterate through set, compare each gene to the parent gene -> if they intersect -> merge them together
        for setItem in geneList:
            if parent.intersect(setItem):
                parent.findOverlap(setItem)
                parent = findParent(parent, setItem)
                removeList.append(setItem)

                # continue
                foundIntersectCycle = True
                break

        # remove added genes
        for i in removeList:
            geneList.remove(i)

    # tabular format
    table = []

    for node in parent.overlappedRepeats.keys():
        for edge in parent.overlappedRepeats[node]:
            table.append([parent.name, node.name, edge])

    return table, parent

main()