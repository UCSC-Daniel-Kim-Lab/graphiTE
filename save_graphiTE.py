import pandas as pd
import numpy as np
import argparse
import class_graphiTE_v2 as g
import joblib

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--csv_file')
    parser.add_argument('-t', '--threshold')

    args = parser.parse_args()

    csvFile = args.csv_file
    threshold = args.threshold

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

    # pass threshold here
    graph = g.Graph(genes, repeats, classifications, array_3d, threshold)

    # create gene nodes for each gene and add to Graph object
    for gene_index in range(len(genes)):
        node = g.Gene(genes[gene_index])
        graph.add_node(node)

    # compare nodes
    graph.compareAll()

    joblib.dump(graph, "save_test")

    # graph.disjointSet()
    # graph.createParentSets()
    # graph.print(outFile)

main()








