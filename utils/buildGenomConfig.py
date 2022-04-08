import fnmatch
from typing import Dict

import yaml
import os,sys

def findPossibleFiles(root:str):
    matches = []
    for root, dirnames, filenames in os.walk(root):
        for filename in fnmatch.filter(filenames, '*.fna'):
            matches.append(os.path.join(root, filename))
    return matches


def getFileSource():
    with open('genom.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config["file"]["sourcefolder"]

def getGenomConfig():
    with open('organismConfig.yaml') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def buildConfig():

    src = getFileSource()
    organisms = getGenomConfig()
