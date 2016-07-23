#!/usr/bin/env python
###
### simulation.py
### 

import sys
import os
import argparse
import numpy

path = os.path.join(os.getcwd(), "lib")
sys.path.insert(0, path)



if __name__ == '__main__':

    desc = """simulation.py ....."""

    parser = argparse.ArgumentParser(description = desc, prog = "simulation.py")
    parser.add_argument('DirName', type=str, help="Enter the name of the directory")

    args = parser.parse_args()

    dirName = args.DirName
    # Reads all parameters, Initial Datum, Flow and MaxCharSpeed
    execfile(os.path.join(dirName, "parameters.py"))

