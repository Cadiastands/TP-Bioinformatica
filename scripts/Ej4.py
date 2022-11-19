import argparse
import os
from Bio import Entrez
from Bio import SeqIO
import time
Entrez.email = "smonjeau@itba.edu.ar"
parser = argparse.ArgumentParser()
parser.add_argument("-input", metavar="INPUT", help="input expected is a blast report",required=True)
parser.add_argument("-pattern", metavar="PATTERN", help="pattern to search",required = True)
#args = parser.parse_args()



input_path= 'blast.out' #args.input
path=os.path.dirname(input_path)
filename=os.path.basename(input_path)

if not os.path.isfile(input_path):
    print ("File doesnt exist/couldn't be opened")
    exit(1)

if not os.access(input_path, os.R_OK):
    print ("File not readable")
    exit(1)


# Perform the BLAST


blast_report_fd = open(input_path,'r')

accessions = []

pattern =  'sapiens' #args.pattern

filtered_output = open('filtered_output.txt','w')

sequences_folder = open('sequences','w')

while True:


    line = blast_report_fd.readline()

    if not line:
        break

    if line == "****Alignment****\n":
        sequence = blast_report_fd.readline()
        if sequence[0:len("sequence")] == "sequence":
            if pattern.lower() in sequence.lower():
                filtered_output.write("****Alignment****")
                filtered_output.write(sequence)
                accession = blast_report_fd.readline()
                if accession[0:len("accession")] == "accession":
                    accessions.append(accession[len("accession")+2:-1].strip())


                while True:
                    line = blast_report_fd.readline()

                    if line == '\n':
                        filtered_output.write(line)
                        break

                    filtered_output.write(line)

filtered_output.close()


for accession in accessions:

    time.sleep(1)
    data = Entrez.efetch(db = "protein", id=int(accession),rettype="gp",retmode="xml")
    record = SeqIO.read(data,"genbank")
    SeqIO.write(record,"sequences/{s}.fasta".format(s=accession) ,'fasta')

    data.close()

 
    

