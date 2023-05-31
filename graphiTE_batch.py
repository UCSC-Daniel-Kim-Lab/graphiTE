import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--csv_file')
# parser.add_argument('-o', '--output_file')

args = parser.parse_args()

csvFile = args.csv_file
# outFile = args.output_file

# load csv file in df
data = pd.read_csv(csvFile)

for i in range(1, 3):
    subset = data.sample(n=10000)

    subset.to_csv("size_10000_batch" + str(i) + ".csv", index=False)

