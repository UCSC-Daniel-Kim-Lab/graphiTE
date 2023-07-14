from pandas import read_csv
from numpy import zeros
from sys import stdout
from datetime import datetime
import argparse

def read_overwrite(fpath):
    # Read Data
    data = read_csv(fpath)
    txs = data['name'].unique()
    reps = data['repName'].unique()
    locs = data['classification'].unique()
    # Make DF
    tx_idx = {tx: idx for idx, tx in enumerate(txs)}
    rep_idx = {rep: idx for idx, rep in enumerate(reps)}
    loc_idx = {loc: idx for idx, loc in enumerate(locs)}
    inserts = zeros((len(txs), len(reps), len(locs)), dtype=int)
    # Fill DF
    for _, row in data.iterrows():
        inserts[
            tx_idx[row['name']],
            rep_idx[row['repName']],
            loc_idx[row['classification']]
        ] += 1
    # Return
    return((
        inserts,
        txs,
        tx_idx,
        reps,
        rep_idx,
        locs,
        loc_idx
    ))


class DisjointSet:
    def __init__(self, tx_dict):
        self.parents = [i for i in tx_dict.values()]
        self.ranks = [1 for _ in self.parents]
    
    def find(tx):
        while tx != self.parents[tx]:
            self.parents[tx] = self.parents[self.parents[tx]]
            tx = self.parents[tx]
        return(tx)

    def union(txA, txB):
        compA, compB = self.find(txA), self.find(txB)
        if (compA==compB): return True
        if (self.ranks[txA] > self.ranks[txB]): self.parents[txB] = txA
        elif (self.ranks[txb] > self.ranks[txA]): self.parents[txA] = txB
        else:
            self.parents[txB] = txA
            self.ranks[txA] += 1
        return False

    def print_components(self, fname=stdout):
        roots = {parent: index for index, parent in enumerate(set(self.parents))}
        components = [[] for _ in range(len(roots.keys()))]
        for tx in range(len(self.parents)):
                components[roots[self.parents[tx]]].append(tx)
        components.sort(key=lambda s: len(s), reverse=True)
        file = fname if fname==stdout else open(fname, 'w')
        print("\t".join([str(len(subset)) for subset in components]), file=file)
        for i in range(max([len(subset) for subset in components])):
            print("\t".join(
                [str(subset[i]) if i < len(subset) else " " for subset in components]
            ), file=file)
        if (file!=stdout): file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output", default=stdout)
    parser.add_argument("-v", "--verbosity", default=-1, type=int)
    parser.add_argument("-t", "--thresh", default=1, type=int)
    args = parser.parse_args()
    start_timer = datetime.now()
    if (args.verbosity > 0): print("Starting GraphiTE")
    if (args.verbosity > 0): print("Reading in Overwrite")
    inserts, txs, tx_idx, reps, rep_idx, locs, loc_idx = read_overwrite(args.input)
    if (args.verbosity > 0): print("Reading Overwrite - COMPLETED")
    if (args.verbosity > 0): print("Initializing Disjoint Set")
    components = DisjointSet(tx_idx)
    if (args.verbosity > 0): print("Disjoint Set - COMPLETED")
    if (args.verbosity > 0): print("Forming Connections")
    for txA in range(len(txs)):
        if ((args.verbosity > 0) & (((txA+1)%args.verbosity)==0)):
            print("Connected {} Genes".format(txA+1))
        for txB in range(txA+1, len(txs)):
            for rep in rep_idx.values():
                found_rep=False
                for loc in loc_idx.values():
                    if (
                        (inserts[txA, rep, loc] > args.thresh) &
                        (inserts[txB, rep, loc] > args.thresh)
                    ):
                        components.union(txA, txB)
                        break
                if found_rep: break
    if (args.verbosity > 0): print("Forming Connections - COMPLETED")
    if (args.verbosity > 0): print("Printing Results")
    components.print_components(args.output)
    stop_timer = datetime.now()
    if (args.verbosity > 0): print("Graphite Completed in {}".format(stop_timer-start_timer))

main()
