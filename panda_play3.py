
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import hashlib
from datetime import datetime

import logging


from pathlib import Path
import sys

import os



__all__ = []
__version__ = 0.1
__date__ = '2024-04-03'
__updated__ = '2024-04-03'

def initLogger(md5string, gffFile):

    ''' setup log file based on project name'''
    projectBaseName = Path(gffFile).stem

    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    logFolder = os.path.join(os.getcwd(), "logfiles")
    if not os.path.exists(logFolder):
        print("--log folder <" + logFolder + "> doesn't exist, creating")
        os.makedirs(logFolder)
    logfileName = os.path.join(logFolder, projectBaseName + "__" + dt_string + "__" + md5string +".log")
    handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.DEBUG)

    fileh = logging.FileHandler(logfileName, 'a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileh.setFormatter(formatter)

    log = logging.getLogger()  # root logger
    log.setLevel(logging.DEBUG)
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fileh)      # set the new handler
    log.addHandler(handler)
    logging.info("+" + "*"*78 + "+")
    logging.info("project log file is <" + logfileName + ">")
    logging.info("+" + "*"*78 + "+")
    logging.debug("debug mode is on")


def parseArgs(argv):
    '''parse out Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    # program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s
    i
      Created by Simon Rayner on %s.
      Copyright 2024 Oslo University Hospital. All rights reserved.

      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0

      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.

    USAGE
    ''' % (program_name, str(__date__))
    try:
        # Setup argument parser
        parser = ArgumentParser(description="GFF loader", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-g", "--gff_list", dest="gfffile", action="store",
                            help="gfflist file name [default: %(default)s]")



        # Process arguments
        args = parser.parse_args()
        gffFile = args.gfffile
        # check the user specified a fasta file, if not warn and and exit
        if gffFile:
            logging.info("gffFileList file is <" + gffFile + ">")
        else:
            logging.error("you must specify a gffFileList file")
            exit

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        print(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

    return gffFile

def generatePlots(gffFile):

    with open(gffFile) as file:
        gffFileList = [line.rstrip() for line in file]

    i=1
    for gffFile in gffFileList:
        logging.info("file <" + str(i) + ">\tis\t" + gffFile)
        df_rno = pd.read_csv(gffFile, delimiter='\t', comment="#", header=None)
        logging.info("read <" + str(len(df_rno)) + "> lines")

        # Set the column names
        df_rno.columns = ['feature', 'empty1', "type", 'start', 'stop', 'empty2', 'strand', 'empty3', 'attributes']
        df_rno['len'] = df_rno['stop'] - df_rno['start'] + 1
        w = 10
        plotname = os.path.basename(gffFile).split('.')[0] + ".png"
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df_rno, x='len', kde=True, bins=np.linspace(0, 200, 20), color='blue', edgecolor='slateblue')
        plt.title('feature length distribution')
        plt.xlabel('length (nt)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(plotname)
        #plt.show()
        i+=1

        # see here for a list of colour names
        # https://matplotlib.org/stable/gallery/color/named_colors.html

    print("plotting completed")






def main(argv=None):
    if argv is None:
        argv = sys.argv
    # parse_args to get filename
    gffFile = parseArgs(argv)
    md5String = hashlib.md5(b"CBGAMGOUS").hexdigest()
    initLogger(md5String, gffFile)
    generatePlots(gffFile)
    logging.info("program completed")





if __name__ == '__main__':
    sys.exit(main())