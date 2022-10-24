# autorigger
body auto rigger built during school
#INITIALISE GUIDE
import maya.cmds as cmds 
import AnoshkaMayatools.AutoRig as AR
reload(AR)
dir(AR)

#BUILD GUIDE
biped = AR.createBipedRig()

#BUILD RIG
AR.buildBipedGuide (biped)
