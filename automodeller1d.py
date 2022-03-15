# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:40:12 2019

@author: Christos
"""

# Point to a folder with alignment files and one protein structure template (specify its filename in the script)
# and make modeller run all the modelling jobs and put the results in new folders with the alignment file name
'''
To run the script and get a log output, it must be run in command line as follows:
>>python automodeller.py > 'some_name.log'
The log will be saved in the current working directory
'''

import os
import glob
import shutil
# Import modeller libraries
from modeller import *              # Load standard Modeller classes
from modeller.automodel import *    # Load the automodel class

# ** Specify the directory where you have the alignment files and the structure of the template protein, keep the '\\' format
#path1 = 'C:\\Users\\Christos\\Desktop\\test\\dummy_files'
path1 = 'C:\\Users\\Christos\\Desktop\\test\\marian'
aln_file_type = '*.ali'         # ** Choose file type for alignment files (i.e. '*.txt' or '*.ali')
template_file = '5u1d.ent'      # ** Specify template filename (PDB structure)
modelNum = 2                   # ** Specify number of models built for each alignment file

# Turn the modeller script into a function
# Homology modeling by the automodel class
def automodeller(alnfile_in, knowns_in, path, end_model, model): # Can add path as 3rd argument
    os.chdir(path)
    
    log.verbose()    # request verbose output
    #log.level(output=1, notes=0, warnings=0, errors=0, memory=0)  
    env = environ()  # create a new MODELLER environment to build this model in

    # directories for input atom files
    env.io.atom_files_directory = './:../atom_files'
    
    a = automodel(env,
                  alnfile  = alnfile_in,           # alignment filename
                  knowns   = knowns_in,            # codes of the templates
                  sequence = model,
                 assess_methods=(assess.DOPE, assess.GA341))              # code of the target
    a.starting_model= 1                 # index of the first model 
    a.ending_model  = end_model         # index of the last model
                                        # (determines how many models to calculate)
    a.make()                            # do the actual homology modeling
    #outputfile = []


os.chdir(path1)                         # Change working directory to specified path
template_noExt = template_file[:-4]     # Remove file extension from template filename for use by modeller

# Find all alignment files in the specified folder for the specified file type (.txt/.ali)
for file1 in glob.glob(aln_file_type):    
    # Grab the name of the .txt file without the extension to use as name for folder creation
    alnfile = file1[:-4]    
    # Create the new path names by merging the current directory with the name of each .txt file
    new_path = path1 + '\\' + alnfile
    
    # Check whether each directory exists and if not, create it, then run the modelling job in it
    if not os.path.exists(new_path):
        os.mkdir(new_path)
        # Copy the alignment and template files in the new folder
        shutil.copy(file1, new_path)
        shutil.copy(template_file, new_path)
        # Run modeller
        automodeller(file1, template_noExt, new_path, modelNum, alnfile)
        os.chdir(path1)
    elif os.path.exists(new_path):
        # Copy the alignment and template files in the new folder
        shutil.copy(file1, new_path)
        shutil.copy(template_file, new_path)
        # Run modeller
        automodeller(file1, template_noExt, new_path, modelNum, alnfile)
        os.chdir(path1)
