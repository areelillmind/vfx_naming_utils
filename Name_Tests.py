   
#### Test


names=[
'SHOW_RL01_000_000_comp_v001_0001_brighter.nk', 
'CRAP_EP03_020_090_comp_v027_9991.nk',
'TC2_EP09_179_44A_roto_v109_0023.nk',
'SB06_EP10_018_010_comp_v003.nk', 
'bollocks', 
'SB06_EP10_018_010_comp_.nk',
'SB06_EP10_018_010_v003.nk',
'SB06_EP10_018_010_v003_optionA.nk',
'BG6_004_0150_comp_v005.nk']

task='comp'
suffix='optionB'


for name in names:
    name=vfx_naming_utils.Shot_Name_Parser(name)

    if name.nameElements:
        print name.nameElements
        name.increment_subver()!={}
        print 'incremented subversion', name.recompile_name()
        name.increment_version()
        print 'incremented version', name.recompile_name()
        name.change_task(task)
        print 'changed task to',task,  name.recompile_name()
        name.change_suffix(suffix)
        print 'changed suffix to',task,  name.recompile_name()
    else:
        print 'Whoopsie!'
        pass

## custom names

customRegex=r'''
([A-Z]+[0-9]+)                # SHOW code, group 0 
(CANTFINDME)?        # ReeL or EPisode number, group 1 
_([0-9]+[A-Z]?)                # scene number, can include letters after the number, group 2
_([0-9]+[A-Z]?)                # shot number, can include letters after the number, group 3
(_[a-z]+)?                # task name, group 4
_(v[0-9]+)                # version number, group 5
(_[0-9]+)?                # subversion number, will be missing from legacy shots, group 6
(_[a-zA-Z]+)?                # suffix, optional and only to be used when submitting multiple creative variants simultaneously e.g. a lighter and darker version, group 7
'''

for name in names:
    name=vfx_naming_utils.Shot_Name_Parser(name, customRegex)

    if name.nameElements:
        print name.nameElements
        name.increment_subver()!={}
        print 'incremented subversion', name.recompile_name()
        name.increment_version()
        print 'incremented version', name.recompile_name()
        name.change_task(task)
        print 'changed task to',task,  name.recompile_name()
        name.change_suffix(suffix)
        print 'changed suffix to',task,  name.recompile_name()
    else:
        print 'Whoopsie!'
        pass
