''' Check and manipulate filenames within the Naming Convention '''

from collections import OrderedDict
import re

## Logging
import logging
logger=logging.getLogger()




MOLI_NAMING_REGEX=r'''
([A-Z]+[0-9]*)				# SHOW code, group 0 
_(RL[0-9]{2}|EP[0-9]{2})		# ReeL or EPisode number, group 1 
_([0-9]+[A-Z]?)				# scene number, can include letters after the number, group 2
_([0-9]+[A-Z]?)				# shot number, can include letters after the number, group 3
(_[a-z]+)?				# task name, group 4
_(v[0-9]+)				# version number, group 5
(_[0-9]+)?				# subversion number, will be missing from legacy shots, group 6
(_[a-zA-Z]+)?				# suffix, optional and only to be used when submitting multiple creative variants simultaneously e.g. a lighter and darker version, group 7
'''

VALID_TASK=re.compile(r'[a-z]{,6}')
VALID_SUFFIX=re.compile(r'[a-zA-Z]{,10}')

class Shot_Name_Parser:
    def __init__(self, name, regex=MOLI_NAMING_REGEX):
	    regex=re.compile(regex, re.VERBOSE)
	    self.parsedName=regex.findall(name)
	    if self.parsedName!=[]:
		    self.parsedName=regex.findall(name)
		    self.nameElements=OrderedDict()
		    self.nameElements['show']=self.parsedName[0][0]
		    self.nameElements['rlep']=self.parsedName[0][1]
		    self.nameElements['scn']=self.parsedName[0][2]
		    self.nameElements['sht']=self.parsedName[0][3]
		    self.nameElements['task']=self.parsedName[0][4][1:]
		    self.nameElements['version']=self.parsedName[0][5]
		    self.nameElements['subver']=self.parsedName[0][6][1:]
		    self.nameElements['suffix']=self.parsedName[0][7][1:]
		    #return self.nameElements
		    
	    else:
		    self.nameElements={}
		    print ('%s : Naming Elements incorrect or not parsed') % name
		    logger.exception('Does not respect VFX naming convention')

    def increment_subver(self):
	    '''Increases the subversion number only '''
	    if self.nameElements!=None:
		    if self.nameElements['subver']=='':
			    newSubVer='0000'
		    else:
			    newSubVer=self.nameElements['subver']
			    newSubVer=int(newSubVer)+1
			    newSubVer='%04d' % newSubVer
		    self.nameElements['subver']=newSubVer
	    else:
		   
		    logger.exception('Naming Elements incorrect or not parsed')
		    
    def increment_version(self):
	    '''Increases the big version number with 3 digit padding e.g. from v0001 to v002, strips suffix, resets subversion '''
	    if self.nameElements!=None:
		    newVer=self.nameElements['version'][1:]
		    newVer=int(newVer)+1
		    newVer='v%03d' % newVer
		    self.nameElements['version']=newVer
		    self.nameElements['suffix']=''
		    self.nameElements['subver']='0000'
	    else:
		    logger.exception('Naming Elements incorrect or not parsed')
		    
		    
    def change_task(self, newTaskName):
	    '''Changes or adds task name, use empty string, use empty string to strip task name'''
	    if self.nameElements!=None:
		    if re.search(VALID_TASK, newTaskName): # empty string is valid too!
			    self.nameElements['task']=newTaskName
		    else:
			    logger.exception('Task name max 6 lowercase letters only, no numbers, whitespace or special characters')
	    else:
		    logger.exception('Naming Elements incorrect or not parsed')

    def change_suffix(self, newSuffix):
	    '''Changes or adds suffix name, use empty string, use empty string to strip task name'''
	    if self.nameElements!=None:
		    if re.search(VALID_SUFFIX, newSuffix): # empty string is valid too!
			    self.nameElements['suffix']=newSuffix
		    else:
			    logger.exception('Suffix name max 10 letters only, no numbers, whitespace or special characters')
	    else:
		    logger.exception('Naming Elements incorrect or not parsed')

    def recompile_name(self):
	    '''Strips unused elements and the recombines into new name string'''
	    values=self.nameElements.values()
	    values=[value for value in values if value!='']
	    return '_'.join(values)

## TO DO
## Set next version which will check name matches (shot, rlep, scn, sht and task) and then ensure that the new version is higher than the any preceeding

## Set Logger
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
