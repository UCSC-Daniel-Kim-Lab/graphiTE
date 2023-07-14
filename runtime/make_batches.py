import argparse as ap
from random import sample

def main():
    parser = ap.ArgumentParser()
    parser.add_argument("-n", "--n", default=10)
    parser.add_argument("-s", "--step", default="10,100,1000")
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    
    with open(args.input, 'r') as file:
            header = file.readline().strip()
            lines = [line.strip() for line in file]
            
    subsets = [int(val) for val in args.step.split(",")]
    for sub in subsets:
        for i in range(int(args.n)):
            print("Making: "+args.output+"/BATCH_"+str(sub)+"_"+str(i)+".csv")
            fname = args.output+"/BATCH_"+str(sub)+"_"+str(i)+".csv"
            nlines = sample(lines, k=sub)
            with open(fname, 'w') as outf:
                print(header, file=outf)
                for nline in nlines:
                    print(nline, file=outf)
main()