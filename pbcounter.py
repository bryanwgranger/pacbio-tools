import HTSeq
import sys
import re
from collections import Counter
import csv

def main(parser):
    args = parser.parse_args()

    fastq_file = HTSeq.FastqReader(args.inFastq if args.inFastq else sys.stdin)
    sorted_fastq = sorted(fastq_file, key=lambda s: len(s))

    fasta_file = HTSeq.FastaReader(args.motifs)
    sequences = [str(s) for s in fasta_file]

    patts = re.compile('(' + ')|('.join(sequences) + ')')

    if args.output:
        outfile_title = args.output
    else:
        outfile_title = 'output'

    with open(f'{outfile_title}.csv', 'w', newline='') as f:
        col_names = ['read'] + sequences + ['total length']
        csv_writer = csv.DictWriter(f, fieldnames=col_names)
        csv_writer.writeheader()
        for read in sorted_fastq:

            count_dict = Counter([s.group() for s in patts.finditer(str(read))])
            count_dict.update({s:0 for s in sequences if s not in count_dict})
            count_dict['read'] = read.name
            count_dict['total length'] = len(read.seq)

            csv_writer.writerow(count_dict)

    print('file done')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='pbcount.py', description='quick count of motifs per read from fastq of extracted repeat sequences')

    parser.add_argument('-i,--inFastq', dest='inFastq', type=str, default=None,
                        help='Input Fastq file. Default stdin')

    parser.add_argument('-m,--motifs', dest='motifs', type=str, default=None,
                        help='Input Fasta file with motifs. Must be in Fasta format', required=True)

    parser.add_argument('-o, --output', dest='output', type=str, default='output',
                        help='Output file name')

    main(parser)