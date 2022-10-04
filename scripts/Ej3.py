import sys
from Bio.Align.Applications import MuscleCommandline as MCL
from Bio import AlignIO as AIO
from os import system

muscle_formats = ["msf", "clw", "html", "fasta"]
aio_formats = ["clustal", "fasta", "maf", "mauve", "phylip", "phylip-sequential", "phylip-relaxed", "stockholm"]


# Parse the arguments

if len(sys.argv) != 7:
    raise Exception("Wrong arguments amount")

in_dir = sys.argv[1]
in_format = sys.argv[2]

muscle_out_file = sys.argv[3]
muscle_format = sys.argv[4]

align_out_file = sys.argv[5]
align_format = sys.argv[6]

if (muscle_format not in muscle_formats):
    raise Exception(f"Invalid muscle output format: {muscle_format}")

if (align_format not in aio_formats):
    raise Exception(f"Invalid alignment output format: {align_format}")


# Perform the MSA

cline = str(MCL(input=in_dir, out=muscle_out_file))

if muscle_format != "fasta":
    cline += " -" + muscle_format
system(cline)

if muscle_format == "html" or muscle_format == "clw":
    print(f'Skipping BioAlign due to invalid format ({muscle_format})')
    exit(0)

alignment = AIO.read(open(muscle_out_file), muscle_format)

print(format(alignment, align_format))
print("Alignment of length %i" % alignment.get_alignment_length())

AIO.write(alignment, align_out_file, align_format)