import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-input", metavar="INPUT", help="input expected is a fasta file", required=True)
parser.add_argument("-output", metavar="OUTPUT", help="output file name", required = True)
args = parser.parse_args()

if not os.path.isfile("prosite.dat") or not os.path.isfile("prosite.doc"):
    print ("prosite.dat or prosite.doc file not found. You can download them from https://ftp.expasy.org/databases/prosite/")
    exit(1)

input_file = args.input
output_file = args.output + ".patmatmotifs"

if input_file.split(".")[-1] != "fasta" and input_file.split(".")[-1] != "fas":
    print("Wrong file type for input")
    exit(1)

os.system("prosextract -prositedir .")
os.system("transeq -sequence " + input_file + " -outseq out/ej5.fa" )
os.system("patmatmotifs -sequence out/ej5.fa -outfile " + output_file)
os.system("rm out/ej5.fa")