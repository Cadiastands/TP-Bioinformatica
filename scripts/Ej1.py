#! /usr/bin/python3

import os
import sys
from Bio import SeqIO



n = len(sys.argv)
if n != 2:
    print("Error: Total arguments passed:",n-1,"Was expecting 1")
    exit(1)
 
input_path=sys.argv[1]
path=os.path.dirname(input_path)
filename=os.path.basename(input_path)
name, ext = os.path.splitext(filename)


with open(input_path, "r") as input_handle:
    with open(name+".fasta", "w") as output_handle:
        sequences = SeqIO.parse(input_handle, "genbank")
        count = SeqIO.write(sequences, output_handle, "fasta")

print("Converted %i records" % count)
