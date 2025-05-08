# autorigger
Biped Auto Rigger built at Capilano University

To use, clone repository and place in maya scripts folder. Run the following: 

//setup in Maya
#INITIALISE GUIDE
import maya.cmds as cmds 
import AnoshkaMayatools.AutoRig as AR
reload(AR)
dir(AR)

//use the template to place your controls
#BUILD GUIDE
biped = AR.createBipedRig()

//Build rig and use control settings to clean up rig. 
#BUILD RIG
AR.buildBipedGuide (biped)

For adding individual limbs, pick a template, place your controls and build rig. 
