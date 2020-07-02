#!/usr/bin/env python
'''
Utility file to rename PVs.
Expects a csv input file with the existing PV name and the new PV name, 
in that order, separated by a comma.
'''

import csv
import os
import sys
import argparse
import json
import subprocess
import shutil
import datetime
import shlex
import logging
import requests

from utils import configureLogging

logger = logging.getLogger(__name__)

def readInputData(file_name):
    with open(filename, 'r') as f:
    pvs = [tuple(line) for line in csv.reader(f)]
    return pvs

def renamePVs(bplURL, pvs):
    '''Rename all PVs in list.'''
    for (old_name, new_name) in pvs:
        url = bplURL + '/pauseArchivingPV'
        print(url)
        #pausedPV = requests.post(url, pv=old_name).json()
        url = bplURL + '/renamePV'
        print(url)
        #renamedPV = requests.post(url, pv=old_name, newname=new_name)
        url = bplURL + '/resumeArchivingPV'
        print(url)
        #renamedPV = requests.post(url, pv=new_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', "--verbose", action="store_true",  help="Turn on verbose logging")
    parser.add_argument("url", help="This is the URL to the mgmt bpl interface of the appliance cluster. For example, http://arch.slac.stanford.edu/mgmt/bpl")
    parser.add_argument("rename_list", help="CSV file with list of PVs to rename")

    args = parser.parse_args()
    configureLogging(args.verbose)

    pvs = readInputData(args.rename_list)

    renamePVs(args.url, pvs)
