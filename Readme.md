# Introduction

this repository contains some simple Python code to demonstrate some basics features of Python (e.g., plotting using Seaborn, Pandas and run time arguments)


## Run Time Arguments

In the code we have been running so far, we have loaded and analysed a single `GFF3` file.  We can change the file path in the code


```
df_rno = pd.read_csv("data/rno.gff3", delimiter='\t', comment="#")
```

but what if we want to analyse several species

in the file `gffs.tar.gz`, there are 33 different species. We could change the file path 33 times, but it's not very efficient

In the new version of the code, `pandas_play2.py`, we load a list of `GFF3` files that we want to process, and then we process them one at a time. Also, instead of 'hardcoding' the file path in the python program, we use the `argparse` package to specify the filename at runtime

```
  python3 panda_play2.py -g '/home/simon/data/mirbase/22/gffs/gfffilelist.txt' 
```
where `gfffilelist.txt` is just a simple list of `GFF3` files


the bulk of the code to do this is specified from lines 6 to 24 in `pandas_play2.py`

```
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

def parseArgs():
    try:
        # Setup argument parser
        parser = ArgumentParser(description="GFF loader", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-g", "--gff_list", dest="gfffile", action="store",
                            help="gfflist file name [default: %(default)s]")

        global gffFile

        # Process arguments
        args = parser.parse_args()
        gffFile = args.gfffile

    except Exception as e:
        print(e)
        return
```
