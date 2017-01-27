import root_numpy as rn

arr = rn.root2array("outfile_newMVA.root", "Events", branches="EventAuxiliary.id_.event_")

if 1310750 in arr:
    print "in here !!!!!!!!"
