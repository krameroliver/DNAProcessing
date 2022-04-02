import os, sys
import tarfile
import fnmatch

rPath = r'E:\Data\HUMAN_MICROBIOM\Bacteria'


def get_type(opath: str):
    matches = []
    for root, dirnames, filenames in os.walk(opath):
        for filename in fnmatch.filter(filenames, '*.fna.tgz'):
            matches.append(os.path.join(root, filename))
    return matches


species = 'Bacteria'

def insert():
    bacterias = get_type(rPath)
    for bacteria in bacterias:
        parts = bacteria.split('\\')[-1].replace(".fna.tgz","")
        organism_type = parts.split("_")[0]
        variant = parts.split("_")[1]
        organism_sub_type = parts.split("_")[2:]
