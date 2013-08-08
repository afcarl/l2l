"""Preparing the context, and launching the qsub command appropriately"""

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../..')))

import re
import subprocess
import xml.etree.ElementTree as ET
#import config

def get_running_jobs():
    """Get running jobs from qstat"""
    try:
        p = subprocess.Popen(["qstat", "-x"], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except OSError:
        return tuple()

    try:
        jobs = ET.fromstring(stdout)
        owner = "fbenurea@"
    except ET.ParseError:
        print("# warning: error parsing qstat xml output (of length {})".format(len(stdout)))
        return []


    my_jobs = []
    for job in jobs:
        if owner == job.find('Job_Owner').text[:len(owner)]:
            my_jobs.append((job.find('Job_Name').text, job.find('Job_Id')))

    return my_jobs

