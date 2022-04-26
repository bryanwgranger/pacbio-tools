# pacbio-tools
Tools for analyzing PacBio sequence data

## PBCounter
This tool will find specified motifs in a given Fastq file and report the counts for each motif in a csv file. The motifs are specified with a Fasta file.

### Dependencies:
[pysam](https://github.com/pysam-developers/pysam)

### Example

```
usage: pbcounter.py [-h] [-i,--inFastq INFASTQ] -m,--motifs MOTIFS
                  [-o, --output OUTPUT]

quick count of motifs per read from fastq of extracted repeat sequences

optional arguments:
  -h, --help            show this help message and exit
  -i,--inFastq INFASTQ  Input Fastq file. Default stdin
  -m,--motifs MOTIFS    Input Fasta file with motifs. Must be in Fasta format
  -o, --output OUTPUT   Output file name
```

```
python pbcounter.py -i test_file_bc1015.extracted_HTT.fastq -m sample_motifs.fasta -o test_file_bc1015_HTT_extracted_counts
```

### Output

Using the provided fastq and motif files as inputs:

| read | CAG | CCG | CCA | CGG | total length |
| --- | --- | --- | --- | --- | --- |
| m64012_191221_044659/114296049/ccs/2280_2376 | 22 | 1 | 8 | 1 | 0 | 96 |
| m64012_191221_044659/114493158/ccs/2278_2374 | 22 | 1 | 8 | 1 | 0 | 96 |
| m64012_191221_044659/143526750/ccs/2234_2330 | 20 | 0 | 7 | 2 | 0 | 96 |

Sample data retrieved from [PacBio](https://www.pacb.com/connect/datasets/).
