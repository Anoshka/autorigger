import maya.cmds as cmds
import utilities
reload(utilities)
#LEG GUIDE 

#Setting names for all controls
group_name = "leg_guide_group"
thigh_loc_name = "thigh_locator"
knee_loc_name = "knee_locator"
ankle_loc_name = "ankle_locator" 
thigh_control_name = "thigh_control" 
knee_control_name = "knee_control"
ankle_control_name = "ankle_control" 
pv_name = "leg_pole_vector"
ik_handle_name = "ik_handle"


def init_guide(mainGroup = None):

    print "DOING INIT"
    utilities.addAnchor(mainGroup, 'anchor_guide_hip', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_rig_hip', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_rig_hip_weight', targetItem = None)
    
    utilities.addAnchor(mainGroup, 'anchor_hidden_rig', targetItem = None)

    # utilities.addAnchor(mainGroup, 'guide_thigh', targetItem = None)
    # utilities.addAnchor(mainGroup, 'rig_thigh_control', targetItem = None)
    # utilities.addAnchor(mainGroup, 'rig_thigh_weight', targetItem = None)



#Creating guide
def build_guide(mainGroup = None,  prefix = " ", s = 1): 
    """creating guide for the leg rig. this is only to set locations."""
    if mainGroup is None:
        mainGroup =     cmds.group(em = True, n = prefix + group_name)
    else:
        prefix = cmds.getAttr(mainGroup+'.prefix')
    if not cmds.attributeQuery('prefix', node = mainGroup, exists = True):
        cmds.addAttr(mainGroup, ln = 'prefix', dt = 'string')
        cmds.setAttr(mainGroup + '.prefix', prefix, type = 'string')

    print "BUILD GUIDE", prefix

    
    #Creatng locators to guide controls 
    thigh_locator = utilities.addLocator    (name = prefix + thigh_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [9, 81, 0],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + thigh_loc_name)

    #creating knee locators, changing scale in local spoace and moving it to default position
    knee_locator = utilities.addLocator    (name = prefix + knee_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [12, 48, 5],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + knee_loc_name)

    #creating ankle locators, changing scale in local spoace and moving it to default position
    ankle_locator = utilities.addLocator    (name = prefix + ankle_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [15, 9, 0],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + ankle_loc_name)

    
    #Creating FK controls - these translations and rotations are locked and can be controlled using the locators
    thigh_control = cmds.circle(name = (prefix + thigh_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(thigh_control + ".rotateZ", 90)
    
    knee_control = cmds.circle(name = (prefix + knee_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(knee_control + ".rotateZ", 90)
    
    ankle_control = cmds.circle(name = (prefix + knee_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(ankle_control + ".rotateZ", 90)
    
    #creating IK controls - the user has access to te roation and translation of these
    pole_vector = cmds.curve(d = 1, p = [(0,4,0), (5, -2, 0), (-5, -2, 0), (0, 4, 0)], k = (0, 1, 2, 3), n = prefix + pv_name)
    
    ik_handle = cmds.curve(d = 1, p = [(5, 5, 5), (-5, 5, 5), (5, 5, -5), (-5, 5, -5), (-5, 5, 5), (-5, -5, 5), (5, -5, 5), (5, 5, 5), (5, 5, -5), (5, -5, -5), (5, -5, 5), (-5, -5, 5), (-5, -5, -5), (5, -5, -5), (5, 5, -5), (-5, 5, -5), (-5, -5, -5)], k = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16))

    #creating heirarchy
    cmds.parent(thigh_control, thigh_locator)
    cmds.parent(knee_control, knee_locator)
    cmds.parent(ankle_control, ankle_locator)
    cmds.parent(pole_vector, knee_control)
    cmds.parent(ik_handle, ankle_locator)
    #cmds.parent(ankle_locator, knee_locator)
    cmds.parent(knee_locator, thigh_locator)

	
    #setting up aim rotations so the thigh always faces the knee, and the knee always faces the ankle
    cmds.aimConstraint(ankle_control, knee_control, worldUpType = "object", worldUpObject = thigh_locator, upVector = (0.0, 1.0, 0.0))
    cmds.aimConstraint(knee_control, thigh_control, worldUpType = "object", worldUpObject = ankle_locator, upVector = (0.0, 1.0, 0.0))
   
    #moving the controls to their positions relative to the locators
    cmds.setAttr(thigh_control + ".translate", 0, 0, 0)
    cmds.setAttr(knee_control + ".translate", 0, 0, 0)
    cmds.setAttr(ankle_control + ".translate", 0, 0, 0)
    cmds.setAttr(pole_vector + ".translate", 0, -36, 0)
    cmds.setAttr(ik_handle + ".translate", 0, -5, 15)
   
    #locking and hiding appropriate controls
    cmds.setAttr(thigh_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(knee_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(ankle_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    #cmds.setAttr(pole_vector + '.rotate', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pole_vector + '.scale', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pole_vector + ".translateZ", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pole_vector + ".visibility", lock = True, keyable = False, channelBox = False)

    #creating group to keep the guide into
    #cmds.parent(thigh_locator, mainGroup)
    #cmds.parent(ankle_locator, mainGroup)
    
    #YOU WANT THE POSITION OF THE LOCATOR AND THE PV AND IK_HANDLE (note to self)
    
    #creating message attribute to be used in the making of the rig - values passed are the positions of the locators, the IK handle and pole vector
    attr_thigh_guide = '{0}.{1}'.format(mainGroup, thigh_loc_name)
    cmds.addAttr(mainGroup, longName = thigh_loc_name, attributeType = 'message')
    cmds.connectAttr(thigh_control + '.message', attr_thigh_guide, force = True)
    
    attr_knee_guide = '{0}.{1}'.format(mainGroup, knee_loc_name)
    cmds.addAttr(mainGroup, longName = knee_loc_name, attributeType = 'message')
    cmds.connectAttr(knee_control + '.message', attr_knee_guide, force = True)
    
    attr_ankle_guide = '{0}.{1}'.format(mainGroup, ankle_loc_name)
    cmds.addAttr(mainGroup, longName = ankle_loc_name, attributeType = 'message')
    cmds.connectAttr(ankle_control + '.message', attr_ankle_guide, force = True)
    
    
	
    attr_ik_guide = '{0}.{1}'.format(mainGroup, ik_handle_name)
    cmds.addAttr(mainGroup, longName = ik_handle_name, attributeType = 'message')
    cmds.connectAttr(ik_handle + '.message', attr_ik_guide, force = True)
	
    attr_pv_guide = '{0}.{1}'.format(mainGroup, pv_name)
    cmds.addAttr(mainGroup, longName = pv_name, attributeType = 'message')
    cmds.connectAttr(pole_vector + '.message', attr_pv_guide, force = True)
	
    attr_kneeLoc_guide = '{0}.{1}'.format(mainGroup, 'loc_' + knee_loc_name)
    cmds.addAttr(mainGroup, longName = 'loc_' + 'left' + knee_loc_name, attributeType = 'message')
    cmds.connectAttr(knee_locator + '.message', attr_kneeLoc_guide, force = True)
    
    attr_ankleLoc_guide = '{0}.{1}'.format(mainGroup, 'loc_' + ankle_loc_name)
    cmds.addAttr(mainGroup, longName = 'loc_' + 'left' + ankle_loc_name, attributeType = 'message')
    cmds.connectAttr(ankle_locator + '.message', attr_ankleLoc_guide, force = True)

    parentItem = utilities.getConnectedAnchorItem(mainGroup, 'anchor_guide_hip')
    print ">>leg>>", parentItem
    if parentItem:
        cmds.parent(thigh_locator, parentItem)
        cmds.parent(ankle_locator, parentItem)
    
def hookup_symmetry(mainGroup, symmetryGroup):
    print "HOOKUP LEG SYMMETRY"
    
    for name in ['.loc_' + thigh_loc_name,
                 '.loc_' + knee_loc_name,
                 '.loc_' + ankle_loc_name,
                 '.' + ik_handle_name,
                 '.' + pv_name]:

        master = cmds.listConnections(symmetryGroup + name, source = True)[0]
        target = cmds.listConnections(mainGroup + name, source = True)[0]
        utilities.createSymmetryConstraint( master, target,  position = True, orientation = True)


    
    


#legguide(prefix = "_left")


#RIG CREATOR FUNCTION
def build_rig (mainGroup, s = 1): 
    """THIS FUNCTION CREATES THE FUNCTION ON THE BASIS OF THE GUIDE POSITIONS"""

    controlParent = utilities.getConnectedAnchorItem( mainGroup, 'anchor_rig_hip' )
    if not controlParent:controlParent = mainGroup
    print "**********************************legguide CP >>>", controlParent
        
    weightParent = utilities.getConnectedAnchorItem( mainGroup, 'anchor_rig_hip_weight' )
    if not weightParent:weightParent = mainGroup
    print "legGuide WP >>>", weightParent
    
    hiddenRigParent = utilities.getConnectedAnchorItem(mainGroup, 'anchor_hidden_rig')
    if not hiddenRigParent:hiddenRigParent = mainGroup
    print "legguide HRP >>>:", hiddenRigParent
        
    #gets the prefix from the extra attribites of the guide group
    prefix = cmds.getAttr(mainGroup + '.prefix')
    
    #this is defined on the basis of the selection 
   

    #this hides the guide group so it doesn't intefere with the new rig  
    cmds.setAttr(mainGroup + '.visibility', 0)
    
    
    #Finds positions of each control 
    
    thigh_location = cmds.listConnections(mainGroup + '.' + thigh_loc_name, source = True)[0]
    
    knee_location = cmds.listConnections(mainGroup + '.' + knee_loc_name, source = True)[0]
    
    ankle_location = cmds.listConnections(mainGroup + '.' + ankle_loc_name, source = True)[0]
    
    ik_ctrl_location = cmds.listConnections(mainGroup + '.' + ik_handle_name, source = True)[0]
    
    pv_location = cmds.listConnections(mainGroup + '.' + pv_name, source = True)[0]
    
    
    #uses xform to get the world position of each control
    
    thigh_translation = cmds.xform(thigh_location, ws = True, translation = True, query = True)
    
    thigh_rotation = cmds.xform(thigh_location, ws = True, rotation = True, query = True)
    
    knee_translation = cmds.xform(knee_location, ws = True, translation = True, query = True)
    
    knee_rotation = cmds.xform(knee_location, ws = True, rotation = True, query = True)
    
    ankle_translation = cmds.xform(ankle_location, ws = True, translation = True, query = True)
    
    ankle_rotation = cmds.xform(ankle_location, ws = True, rotation = True, query = True)
    
    ik_translation = cmds.xform(ik_ctrl_location, ws = True, translation = True, query = True)
    
    ik_rotation = cmds.xform(ik_ctrl_location, ws = True, rotation = True, query = True)
    
    pv_translation = cmds.xform(pv_location, ws = True, translation = True, query = True)
    
    pv_rotation = cmds.xform(pv_location, ws = True, rotation = True, query = True)
    
    
    #Creates controls on the basis of found positions 
	
    thigh_control = cmds.circle(name = (prefix + "thigh_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(thigh_control + '.translate', *thigh_translation)
    cmds.setAttr(thigh_control + '.rotate', *thigh_rotation)
    
    knee_control = cmds.circle(name = (prefix + "knee_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(knee_control + '.translate', *knee_translation)
    cmds.setAttr(knee_control + '.rotate', *knee_rotation)
    
    ankle_control = cmds.circle(name = (prefix + "ankle_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(ankle_control + '.translate', *ankle_translation)
    cmds.setAttr(ankle_control + '.rotate', *ankle_rotation)
    
    size = s*5
    ik_position = p = [(size, size, size), (-size, size, size), (size, size, -size), (-size, size, -size), (-size, size, size), (-size, -size, size), (size, -size, size), (size, size, size), (size, size, -size), (size, -size, -size), (size, -size, size), (-size, -size, size), (-size, -size, -size), (size, -size, -size), (size, size, -size), (-size, size, -size), (-size, -size, -size)]
    
    ik_ctrl = cmds.curve(d = 1, p = ik_position, k = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), n = prefix + "leg_IK_CTRL")
    cmds.setAttr(ik_ctrl + '.translate', *ik_translation)
    cmds.setAttr(ik_ctrl + '.rotate', *ik_rotation)
    
    pv_ctrl = cmds.curve(d = 1, p = [(s*0,s*4,s*0), (s*5, s*-2, s*0), (s*-5, s*-2, s*0), (s*0, s*4, s*0)], k = (0, 1, 2, 3), n = prefix + "leg_pole_vector_CTRL")
    cmds.setAttr(pv_ctrl + '.translate', *pv_translation)
    cmds.setAttr(pv_ctrl + '.rotate', *pv_rotation)
    
    
    #Zeroes out controls 
    
    leg_rig_group = cmds.group(em = True, n = prefix + "leg_mainGroup")
    thigh_zero = cmds.group(em = True, n = prefix + "thigh_CTRL_ZERO")
    knee_zero = cmds.group(em = True, n = prefix + "knee_CTRL_ZERO")
    ankle_zero = cmds.group(em = True, n = prefix + "ankle_CTRL_ZERO")
    ik_zero = cmds.group(em = True, n = prefix + "IK_CTRL_ZERO")
    pv_zero = cmds.group(em = True, n = prefix + "PV_CTRL_ZERO")
    
    cmds.matchTransform(thigh_zero, thigh_control)
    cmds.matchTransform(knee_zero, knee_control)
    cmds.matchTransform(ankle_zero, ankle_control) 
    cmds.matchTransform(ik_zero, ik_ctrl)
    cmds.matchTransform(pv_zero, pv_ctrl)
    
    cmds.parent(leg_rig_group, controlParent)
    print "            test >>", leg_rig_group
    print "            test >>", controlParent
    cmds.parent(thigh_control, thigh_zero)
    cmds.parent(knee_control, knee_zero)
    cmds.parent(ankle_control, ankle_zero)
    cmds.parent(ik_ctrl, ik_zero)
    cmds.parent(pv_ctrl, pv_zero)
    
    cmds.parent(thigh_zero, leg_rig_group)
    cmds.parent(knee_zero, thigh_control)
    cmds.parent(ankle_zero, knee_control)
    cmds.parent(ik_zero, leg_rig_group)
    cmds.parent(pv_zero, leg_rig_group)
    
  
    #Creates IK joints and positions them 
    
    thigh_jt = cmds.joint(p = (0, 10, 0), n = prefix + "thigh_IK_jt")
    
    knee_jt = cmds.joint(p = (0, 5, 0), n = prefix + "knee_IK_jt")
    
    ankle_jt = cmds.joint(p = (0, 0, 0), n = prefix + "ankle_IK_jt")
        
    cmds.parent(thigh_jt, w = True)	
    
    cmds.matchTransform(thigh_jt, thigh_control)
    cmds.matchTransform(knee_jt, knee_control)
    cmds.matchTransform(ankle_jt, ankle_control)
        
    #sets preferred angle so the joints dont snap when the handle is created
    cmds.setAttr(knee_jt + '.preferredAngleZ', cmds.getAttr(knee_jt + '.rotateZ'))
  

    
    # cmds.joint(prefix + "thigh_IK_jt", e = True, spa = True)
    # cmds.joint(prefix + "knee_IK_jt", e = True, spa = True) 
    # cmds.joint(prefix + "ankle_IK_jt", e = True, spa = True)
    
    
    #Creates IK Handle for IK joints 
    
    ik_handle = cmds.ikHandle(n = prefix + "leg_ikhandle", sj = thigh_jt, ee = ankle_jt) 
    
    print "IK",ik_handle
    print "CTRL",ik_ctrl
    
    cmds.parent(ik_handle[0], ik_ctrl)
    
    
    #Creates pole vector control - seems to only work with the name pf the given ik handle types directly as the slave
    
    pole_vector = cmds.poleVectorConstraint(pv_ctrl, prefix + "leg_ikhandle") 
    
    cmds.select(clear = True)
    
    
    #Creates weighting joints and positions them 
    
    thigh_wt = cmds.joint(p = (0, 10, 0), n = prefix + "thigh_wt")
    
    knee_wt = cmds.joint(p = (0, 5, 0), n = prefix + "knee_wt")
    
    ankle_wt = cmds.joint(p = (0, 0, 0), n = prefix + "ankle_wt")
    
    cmds.matchTransform(thigh_wt, thigh_jt)
    cmds.matchTransform(knee_wt, knee_jt)
    cmds.matchTransform(ankle_wt, ankle_jt)
    
    
    #Sets preferred angle for weight joints 
    
    # cmds.joint(thigh_wt, e = True, spa = True)
    # cmds.joint(knee_wt, e = True, spa = True) 
    # cmds.joint(ankle_wt, e = True, spa = True)
    

    
    #orient constrains wt joints to the ik joints and fk controls, and assigns it to a variable so it can be used to set up attribute connections 
        
    thigh_oc = cmds.orientConstraint(thigh_jt, thigh_wt, weight = 1)
    knee_oc= cmds.orientConstraint(knee_jt, knee_wt, weight = 1)
    ankle_oc = cmds.orientConstraint(ankle_jt, ankle_wt, weight = 1)
    
    thigh_oc = cmds.orientConstraint(thigh_control, thigh_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    knee_oc = cmds.orientConstraint(knee_control, knee_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    ankle_oc = cmds.orientConstraint(ankle_control, ankle_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    
    print thigh_oc
    
    
    #Creates option box, adds Fk_Ik attributue and creates a switch by connecting attributes 
    #FK = 0, IK = 1
    
    option_box = cmds.curve(d = 1, p = [( s*9,-s*31, s*0), (s*0, -s*36, s*0), (s*0,  -s*26, s*0), (s*9, -s*31, s*0 )], k = (0, 1, 2, 3), n = prefix + 'leg' + 'option_box')
    cmds.parentConstraint(ankle_wt, option_box, maintainOffset = False)
    
    #cmds.move(option_box, x = -20)
    #cmds.setAttr(option_box + '.translateX', -20)
    
    cmds.addAttr(option_box, ln = "Fk_Ik", at = 'double', min = 0, max = 1, dv = 0)
    cmds.setAttr(option_box + '.Fk_Ik', keyable = True)
    
    cmds.connectAttr(option_box + '.Fk_Ik', thigh_oc[0] + "." +  prefix + "thigh_IK_jtW0", force = True)
    cmds.connectAttr(option_box + '.Fk_Ik', knee_oc[0] + "." +  prefix + "knee_IK_jtW0", force = True)
    cmds.connectAttr(option_box + '.Fk_Ik', ankle_oc[0] + "." +  prefix + "ankle_IK_jtW0", force = True)
    
    
    pma = cmds.shadingNode('plusMinusAverage', asUtility = True)
    
    print pma 


    # cmds.parent(ik_handle, hiddenRigParent)
    cmds.parent(thigh_jt, hiddenRigParent)
    
    cmds.connectAttr(option_box + '.Fk_Ik', pma + '.input1D[0]')
    cmds.disconnectAttr(option_box + '.Fk_Ik', pma + '.input1D[0]')
    cmds.connectAttr(option_box + '.Fk_Ik', pma + '.input1D[1]')
    cmds.setAttr(pma + '.operation', 2)
    cmds.setAttr(pma + '.input1D[0]', 1)
    
    cmds.connectAttr(pma + '.output1D', thigh_oc[0] + "." +  prefix + "thigh_CTRLW1", force = True)
    cmds.connectAttr(pma + '.output1D', knee_oc[0] + "." +  prefix + "knee_CTRLW1", force = True)
    cmds.connectAttr(pma + '.output1D', ankle_oc[0] + "." +  prefix + "ankle_CTRLW1", force = True)
    
    
    cmds.connectAttr(option_box + '.Fk_Ik', ik_ctrl + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', pv_ctrl + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', thigh_jt + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', knee_jt + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', ankle_jt + '.visibility')
    
    cmds.connectAttr(pma + '.output1D', thigh_control + '.visibility')
    cmds.connectAttr(pma + '.output1D', knee_control + '.visibility')
    cmds.connectAttr(pma + '.output1D', ankle_control + '.visibility')
    
    cmds.parent(option_box, controlParent)
    
    #Locks and hides unnessecary attributes 
    
    cmds.setAttr(thigh_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(thigh_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(knee_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(knee_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
    
    cmds.setAttr(ankle_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ankle_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(ik_ctrl + '.rotateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ik_ctrl + '.rotateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ik_ctrl + '.rotateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ik_ctrl + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ik_ctrl + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ik_ctrl + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(ik_ctrl + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(pv_ctrl + '.rotateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pv_ctrl + '.rotateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pv_ctrl + '.rotateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pv_ctrl + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pv_ctrl + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pv_ctrl + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(pv_ctrl + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(option_box + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.rotateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.rotateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.rotateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(option_box + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.pointConstraint(thigh_control, thigh_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    
    cmds.setAttr(ik_handle[0] + '.visibility', 0)
    print "weightParent is --->>>", weightParent
    
    
    cmds.parent(thigh_wt, weightParent)

    
    FK_colour = utilities.addColorAttr(option_box, "FK_Colour", red = 1, green = 0, blue = 0)
    IK_colour = utilities.addColorAttr(option_box, "IK_Colour", red = 0, green = 1, blue = 0)
    main_colour = utilities.addColorAttr(option_box, "Main_Colour", red = 0, green = 0, blue = 1)
            
    utilities.attachColourToShape(FK_colour, thigh_control)
    utilities.attachColourToShape(FK_colour, knee_control)
    utilities.attachColourToShape(FK_colour, ankle_control)
    utilities.attachColourToShape(IK_colour, ik_ctrl)
    utilities.attachColourToShape(IK_colour, pv_ctrl)
    utilities.attachColourToShape(main_colour, option_box)
    
    
    
#leg_rig(mainGroup = cmds.ls(selection = True)[0], s = 1)
	
		
	
	
#thigh_wt_orientConstraint1.thigh_IK_jtW0
	
#[[u'thigh_wt_orientConstraint1'], [u'thigh_wt_orientConstraint1']]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
