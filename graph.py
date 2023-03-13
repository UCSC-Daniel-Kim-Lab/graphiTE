import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import graphiTE as graphiTE

table, parent = graphiTE.main()

def findPositions(parent):
    """ find positions to know where to draw nodes """

    # create node:array_of_x_y_coords dictionary
    coordinates = {}

    # list holding parent's children
    children = []
    children.extend(parent.children)

    # move parent's position to top of figure
    coordinates[parent] = np.array([0, 1])

    # get distance between each level of nodes
    y_dist = 1 / (parent.maxDepth + 1)

    # set current y to the next level after parent
    currY = 1 - y_dist

    while len(children) != 0:
        # get distance between children
        x_dist = 1 / len(children)
        size = len(children)

        modify = -1

        for i in range(0, size):

            node = children.pop(0)

            # go left when (-), go right when (+)
            plotX = coordinates[node.parent][0] + ((modify * x_dist) * ((i // 2) + 1))

            # add new position to dictionary
            coordinates[node] = np.array([plotX, currY])

            # add children back to list
            children.extend(node.children)

            # each increment flips negative <-> positive
            modify *= -1

        currY -= y_dist

    return coordinates

def draw_tree(parent):
    """ draw nodes and edges """
    G = nx.DiGraph()

    # start stack at highest node in tree (parent)
    stack = [parent]

    # dfs, creates edges between nodes and its children
    # adds children onto stack
    while stack:
        # remove top node
        node = stack.pop()
        # add node to graph
        G.add_node(node)
        # iterate over children
        for child in node.children:
            # for every child create an edge between node and child
            G.add_edge(node, child, name=', '.join(node.overlappedRepeats[child]))
            # add child onto stack
            stack.append(child)

    # find positions in figure of every node
    pos = findPositions(parent)
    # create position dictionary
    pos_dict = {node: (pos[node][0], pos[node][1]) for node in pos}

    plt.figure(figsize=(8, 8))

    nx.draw(G, pos_dict, with_labels=True, node_size=500)
    edge_labels = nx.get_edge_attributes(G, "name")
    nx.draw_networkx_edge_labels(G, pos_dict, edge_labels=edge_labels)

    plt.show()

draw_tree(parent)