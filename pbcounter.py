import HTSeq
import sys
import re
from collections import Counter
import csv

def main(parser):
    args = parser.parse_args()

    ## read the Fastq file and the sort it based on read length (smaller reads first)
    fastq_file = HTSeq.FastqReader(args.inFastq if args.inFastq else sys.stdin)
    sorted_fastq = sorted(fastq_file, key=lambda s: len(s))

    ## read the motifs from the Fasta file and create a list of them
    ## this preserves the order of the motifs
    fasta_file = HTSeq.FastaReader(args.motifs)
    sequences = [str(s) for s in fasta_file]

    # create a regular expression for each motif
    patts = re.compile('(' + ')|('.join(sequences) + ')')

    #process the output file title
    if args.output:
        if args.output.endswith('.csv'):
            outfile_title = args.output[:-4]
    else:
        outfile_title = 'extracted_motif_output'

    # create a csv file object, establish the column names
    with open(f'{outfile_title}.csv', 'w', newline='') as f:
        col_names = ['read'] + sequences + ['total length']
        csv_writer = csv.DictWriter(f, fieldnames=col_names)
        csv_writer.writeheader()

        # iterate through each read of the sorted fastq file
        for read in sorted_fastq:

            #search the read for the motifs using regex
            count_dict = Counter([s.group() for s in patts.finditer(str(read))])
            #update the dictionary for any motifs with zero counts
            count_dict.update({s:0 for s in sequences if s not in count_dict})
            #add the read name and total length to the dictionary
            count_dict['read'] = read.name
            count_dict['total length'] = len(read.seq)

            # write the data to a row in the csv file
            csv_writer.writerow(count_dict)

    print(f'Output file {outfile_title}.csv has been created.')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='pbcount.py', description='quick count of motifs per read from fastq of extracted repeat sequences')

    parser.add_argument('-i,--inFastq', dest='inFastq', type=str, default=None,
                        help='Input Fastq file.')

    parser.add_argument('-m,--motifs', dest='motifs', type=str, default=None,
                        help='Input Fasta file with motifs. Must be in Fasta format', required=True)

    parser.add_argument('-o, --output', dest='output', type=str, default='output',
                        help='Output file name (extension not necessary)')

    main(parser)