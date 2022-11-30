#! /usr/bin/python3

import os
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import argparse


#code from https://www.biostars.org/p/398203/

def translate_record(record):
    table = 1
    min_pro_len = 25

    max_seq = []
    for strand, nuc in [(+1, record.seq), (-1, record.seq.reverse_complement())]:
        for frame in range(3):
            length = 3 * ((len(record)-frame) // 3)
            for pro in nuc[frame:frame+length].translate(table).split("*"):
                splitlocal = pro.find('M')
                seq_final = pro[splitlocal:]
                if len(seq_final) >= min_pro_len and len(max_seq) < len(seq_final):
                    max_seq = seq_final
    return SeqRecord(seq = max_seq, \
                   id =  record.id + "_translated", \
                   description = record.description + " translated to protein")


# Parse the arguments

parser = argparse.ArgumentParser()
parser.add_argument("-input", metavar="INPUT", help="input file must be a GENBANK file (.gbk/.gb)",required=True)
parser.add_argument("-output", metavar="OUTPUT", help="output file name",required = True)
args = parser.parse_args()

input_path = args.input
path = os.path.dirname(input_path)
filename = os.path.basename(input_path)
name, ext = os.path.splitext(filename)

if input_file.split(".")[-1] != "gb" and input_file.split(".")[-1] != "gbk":
    print("Wrong file type for input")
    exit(1)

if not os.path.isfile(input_path):
    print ("File doesnt exist/couldn't be opened")
    exit(1)

if not os.access(input_path, os.R_OK):
    print ("File not readable")
    exit(1)


# Read mRNA, traduce to proteins and save as FASTA file

records = SeqIO.parse(input_path, 'gb')
records_amino = SeqIO.parse(input_path, 'gb')


SeqIO.write(records, open(args.output + '_nucleic.fas', 'w'), 'fasta')

aminoacid_seq = [translate_record(rec) for rec in records_amino]

SeqIO.write(aminoacid_seq, open(args.output + '_aminoacids.fas', 'w'), 'fasta')