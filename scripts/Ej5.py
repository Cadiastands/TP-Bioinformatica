import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("-input", metavar="INPUT", help="input expected is a fasta file", required=True)
parser.add_argument("-output", metavar="OUTPUT", help="output file name", required = True)
args = parser.parse_args()

input_file = args.input
output_file = args.output + ".patmatmotifs"

if input_file.split(".")[1] != "fasta" and input_file.split(".")[1] != "fas":
    print("Wrong file type for input")
    exit(1)

os.system("transeq -sequence " + faa_filename + " -outseq out/ej5.transeq.fa" )
os.system("patmatmotifs -sequence out/ej5.transeq.fa -outfile " + output_file)