#! /usr/bin/python3

import os
import sys
from Bio import SeqIO


#check valid arguments
n = len(sys.argv)
if n != 2:
    print("Error: Total arguments passed:",n-1,"Was expecting 1")
    exit(1)

#Extracting the name of the file
input_path=sys.argv[1]
path=os.path.dirname(input_path)
filename=os.path.basename(input_path)
name, ext = os.path.splitext(filename)

if not os.path.isfile(input_path):
    print ("File doesnt exist/couldn't be opened")
    exit(1)

if not os.access(input_path, os.R_OK):
    print ("File not readable")
    exit(1)




#converting the file to fasta

result_count=SeqIO.convert(input_path, "genbank", name+".fasta", "fasta")

print("Converted %i records" % result_count)
