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
import time

from utils import configureLogging

logger = logging.getLogger(__name__)

def readInputData(file_name):
    with open(file_name, 'r') as f:
        pvs = [tuple(line) for line in csv.reader(f)]
    return pvs

def renamePVs(bplURL, pvs):
    '''Rename all PVs in list.'''
    for (old_name, new_name) in pvs:
        old_name = old_name.strip()
        new_name = new_name.strip()
        
        print('Renaming from {} to {}'.format(old_name, new_name))

        url = bplURL + '/pauseArchivingPV'
        parameters = {'pv': old_name}
        pausedPV = requests.get(url, params=parameters)

	time.sleep(0.1)
	
        url = bplURL + '/renamePV'
        parameters = {'pv': old_name, 'newname': new_name}
        renamedPV = requests.get(url, params = parameters)

	time.sleep(0.1)

        url = bplURL + '/resumeArchivingPV'
        parameters = {'pv': new_name}
        resumedPV = requests.get(url, params = parameters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', "--verbose", action="store_true",  help="Turn on verbose logging")
    parser.add_argument("url", help="This is the URL to the mgmt bpl interface of the appliance cluster. For example, http://arch.slac.stanford.edu/mgmt/bpl")
    parser.add_argument("rename_list", help="CSV file with list of PVs to rename")

    args = parser.parse_args()
    configureLogging(args.verbose)

    pvs = readInputData(args.rename_list)

    renamePVs(args.url, pvs)
