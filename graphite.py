from pandas import read_csv
from numpy import zeroes


def read_overwrite(fpath):
    # Read Data
    dat = read_csv(fpath)
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
            tx_idx[row['name2']],
            rep_idx[row['repName']],
            loc_idx[row['classification']]
        ] += 1
    # Return
    return((
        inserts,
        tx_idx,
        rep_idx,
        loc_idx
    ))


class DisjointSet:
    def __init__(self, tx_dict):
        self.parents = [i for i in tx_dict.values()]
        self.ranks = [1 for _ in range(len(self.nodes))]
    
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


def main():
    print("Hello world")
    