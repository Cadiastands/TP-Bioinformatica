import os
import sys
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Applications import NcbiblastnCommandline
import argparse



def parse_output (blast_result,value_limit,mode,filename):
    output = ""
    for blast_record in blast_result:    
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                
                if hsp.expect < value_limit:
                    output += "****Alignment****\n"
                    output += "sequence: %s\n" % alignment.hit_def.split(' >')[0]
                    output += "accession: %s\n" % alignment.hit_id.split('|')[1]
                    output += "length: %d\n" % alignment.length
                    output += "score: %s\n" % str(hsp.score)
                    output += "identity: %d/%d(%.2f%%)\n" % (hsp.identities, hsp.align_length, (100 * hsp.identities / hsp.align_length))
                    output += "E-value: %f\n" % hsp.expect
                    output += "query: %s\n" % hsp.query
                    output += "match: %s\n" % hsp.match
                    output += "sbjct: %s\n\n" % hsp.sbjct

    with open(filename, "w") as file:
        file.write(output)



parser = argparse.ArgumentParser()
parser.add_argument("-input", metavar="INPUT", help="input file, must be a FASTA file (.fas)",required=True)
parser.add_argument("-output", metavar="OUTPUT", help="output file name",required=True)
parser.add_argument("-mode",choices=['local','remote'] ,metavar="MODE", help="mode must be <local> or <remote>. Default is remote",default='remote')
parser.add_argument("-db",metavar="DB_PATH",help="path to db. Only use if mode is local")
args = parser.parse_args()

if args.mode == "local" and args.db == None:
    parser.error("Must provide db path in -db argument")


E_VALUE_LIMIT = 0.04




#Extracting the name of the file
input_path=args.input
path=os.path.dirname(input_path)
filename=os.path.basename(input_path)

#Local or remote BLAST
mode = args.mode

if not os.path.isfile(input_path):
    print ("File doesnt exist/couldn't be opened")
    exit(1)

if not os.access(input_path, os.R_OK):
    print ("File not readable")
    exit(1)

# input_path = "fastita.fas"
fasta_fd = open(input_path).read()



if mode == "remote":
    blast_query_handle = NCBIWWW.qblast("blastp", "swissprot", fasta_fd)
    blast_result = NCBIXML.parse(blast_query_handle)
    #with open('results.xml', 'w') as save_file: 
    #    blast_results = blast_query_handle.read() 
    #    save_file.write(blast_results)
    parse_output(blast_result,E_VALUE_LIMIT,mode,args.output)

    
else:
    PATH_TO_DB = "/home/santiago/Downloads/ncbi-blast-2.13.0+/data/"
    blastn_cline = NcbiblastpCommandline(query = input_path, db = args.db + "swissprot", outfmt = 5, out = "results.xml")
    stdout, stderr = blastn_cline()
    blast_result = NCBIXML.parse(open("results.xml"))
    parse_output(blast_result,E_VALUE_LIMIT,mode,args.output)



