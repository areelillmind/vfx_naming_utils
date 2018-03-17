''' Check and manipulate filenames within the Naming Convention '''

from collections import OrderedDict
import re
import logging
logger=logging.getLogger()

NAMING_REGEX=re.compile(r'''
([A-Z]+[0-9]*)				# SHOW code, group 0 
_(RL[0-9]{2}|EP[0-9]{2})	# ReeL or EPisode number, group 1 
_([0-9]+[A-Z]?)				# scene number, can include letters after the number, group 2
_([0-9]+[A-Z]?)				# shot number, can include letters after the number, group 3
(_[a-z]+)?					# task name, group 4
_(v[0-9]+)					# version number, group 5
(_[0-9]+)?					# subversion number, will be missing from legacy shots, group 6
(_[a-zA-Z]+)?			# suffix, optional and only to be used when submitting multiple creative variants simultaneously e.g. a lighter and darker version, group 7
''', re.VERBOSE)

VALID_TASK=re.compile(r'[a-z]{,6}')
VALID_SUFFIX=re.compile(r'[a-zA-Z]{,10}')

def parse_name(name, regex):
	parsedName=regex.findall(name)
	if parsedName!=[]:
		parsedName=regex.findall(name)
		nameElements=OrderedDict()
		nameElements['show']=parsedName[0][0]
		nameElements['rlep']=parsedName[0][1]
		nameElements['scn']=parsedName[0][2]
		nameElements['sht']=parsedName[0][3]
		nameElements['task']=parsedName[0][4][1:]
		nameElements['version']=parsedName[0][5]
		nameElements['subver']=parsedName[0][6][1:]
		nameElements['suffix']=parsedName[0][7][1:]
		return nameElements
		
	else:
		logger.exception('Does not respect VFX naming convention')

def increment_subver(nameElements):
	'''Increases the subversion number only '''
	if nameElements!=None:
		if nameElements['subver']=='':
			newSubVer='0000'
		else:
			newSubVer=nameElements['subver']
			newSubVer=int(newSubVer)+1
			newSubVer='%04d' % newSubVer
		nameElements['subver']=newSubVer
	else:
		logger.exception('Naming Elements incorrect or not parsed')
		
def increment_version(nameElements):
	'''Increases the big version number with 3 digit padding e.g. from v0001 to v002, strips suffix, resets subversion '''
	if nameElements!=None:
		newVer=nameElements['version'][1:]
		newVer=int(newVer)+1
		newVer='v%03d' % newVer
		nameElements['version']=newVer
		nameElements['suffix']=''
		nameElements['subver']='0000'
	else:
		logger.exception('Naming Elements incorrect or not parsed')
		
def change_task(nameElements, newTaskName):
	'''Changes or adds task name, use empty string, use empty string to strip task name'''
	if nameElements!=None:
		if re.search(VALID_TASK, newTaskName): # empty string is valid too!
			nameElements['task']=newTaskName
		else:
			logger.exception('Task name max 6 lowercase letters only, no numbers, whitespace or special characters')
	else:
		logger.exception('Naming Elements incorrect or not parsed')

def change_suffix(nameElements, newSuffix):
	'''Changes or adds suffix name, use empty string, use empty string to strip task name'''
	if nameElements!=None:
		if re.search(VALID_SUFFIX, newSuffix): # empty string is valid too!
			nameElements['suffix']=newSuffix
		else:
			logger.exception('Suffix name max 10 letters only, no numbers, whitespace or special characters')
	else:
		logger.exception('Naming Elements incorrect or not parsed')

def recompile_name(nameElements):
	'''Strips unused elements and the recombines into new name string'''
	values=nameElements.values()
	values=[value for value in values if value!='']
	return '_'.join(values)

## TO DO
## Set next version which will check name matches (shot, rlep, scn, sht and task) and then ensure that the new version is higher than the any preceeding

## Set Logger
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    
#### Test


names=[
'SHOW_RL01_000_000_comp_v001_0001_brighter.nk', 
'CRAP_EP03_020_090_comp_v027_9991.nk',
'TC2_EP09_179_44A_roto_v109_0023.nk',
'SB06_EP10_018_010_comp_v003.nk', 
'bollocks', 
'SB06_EP10_018_010_comp_.nk',
'SB06_EP10_018_010_v003.nk',
'SB06_EP10_018_010_v003_optionA.nk']

task='comp'
suffix=''


for name in names:
	name=parse_name(name, NAMING_REGEX)
	print name
	if name!=None:
		increment_subver(name)
		print 'incremented subversion', recompile_name(name)
		increment_version(name)
		print 'incremented version', recompile_name(name)
		change_task(name, task)
		print 'changed task to',task,  recompile_name(name)
		change_suffix(name, suffix)
		print 'changed suffix to',suffix,  recompile_name(name)
