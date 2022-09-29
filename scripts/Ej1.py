#! /usr/bin/python3

import os
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("-input", metavar="INPUT", help="input file must be a GENBANK file (.gbk)",required=True)
parser.add_argument("-output", metavar="OUTPUT", help="output file name",required = True)
args = parser.parse_args()



#Extracting the name of the file
input_path=args.input
path=os.path.dirname(input_path)
filename=os.path.basename(input_path)
name, ext = os.path.splitext(filename)

if not os.path.isfile(input_path):
    print ("File doesnt exist/couldn't be opened")
    exit(1)

if not os.access(input_path, os.R_OK):
    print ("File not readable")
    exit(1)
    

#code from https://www.biostars.org/p/398203/
def translate_record(record):
    table = 1
    min_pro_len = 54
    x= 0

    aux = []
    max_seq = []
    for strand, nuc in [(+1, record.seq), (-1, record.seq.reverse_complement())]:
        for frame in range(3):
            length = 3 * ((len(record)-frame) // 3) 
            for pro in nuc[frame:frame+length].translate(table).split("*"):
                splitlocal = pro.find('M')
                seq_final = pro[splitlocal:]
                if len(seq_final) >= min_pro_len:
                    aux.append(seq_final)

                    x = x+1
                if len(max_seq) < len(seq_final):
                    max_seq = seq_final   
    return SeqRecord(seq = max_seq, \
                   id =  record.id + "_translated", \
                   description = record.description + " translated to protein")                



records = SeqIO.parse(input_path, 'gb')

aminoacid_seq = []
for rec in records:
  aminoacid_seq.append(translate_record(rec))

SeqIO.write(aminoacid_seq, open(args.output + '.fas', 'w'), 'fasta')

#converting the file to fasta

#result_count=SeqIO.convert(input_path, "genbank", name+".fas", "fasta")

#print("Converted %i records" % result_count)
