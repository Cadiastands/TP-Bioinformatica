import os
import sys
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

#check valid arguments
n = len(sys.argv)
if n != 2:
    print("Error: Total arguments passed:",n-1,"Was expecting 1")
    exit(1)

#Extracting the name of the file
input_path=sys.argv[1]
path=os.path.dirname(input_path)
filename=os.path.basename(input_path)


if not os.path.isfile(input_path):
    print ("File doesnt exist/couldn't be opened")
    exit(1)

if not os.access(input_path, os.R_OK):
    print ("File not readable")
    exit(1)

# input_path = "fastita.fas"
fasta_fd = open(input_path).read()
blast_query_handle = NCBIWWW.qblast("blastn", "nr", fasta_fd)
blast_result = NCBIXML.parse(blast_query_handle)

E_VALUE_LIMIT = 0.04

output = ""
for blast_record in blast_result:    
    for alignment in blast_result.alignments:
        for hsp in alignment.hsps:
            
            if hsp.expect < E_VALUE_LIMIT:
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

with open("blast.out", "w") as file:
    file.write(output)
