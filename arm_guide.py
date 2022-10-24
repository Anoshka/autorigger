import maya.cmds as cmds
import utilities
import spine_guide
reload(utilities)
#arm GUIDE 

#Setting names for all controls
group_name = "arm_guide_group"
shoulder_loc_name = "shoulder_locator"
arm_loc_name = "arm_locator"
elbow_loc_name = "elbow_locator"
wrist_loc_name = "wrist_locator" 
shoulder_control_name = "shoulder_control"
arm_control_name = "arm_control" 
elbow_control_name = "elbow_control"
wrist_control_name = "wrist_control" 
pv_name = "arm_pole_vector"
ik_handle_name = "ik_handle"


def init_guide(mainGroup = None):
    """initialising all anchors to other modules"""
    utilities.addAnchor(mainGroup, 'anchor_guide_chest', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_rig_chest_control', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_rig_chest_weight', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_hidden_rig', targetItem = None)
    




#Creating guide
def build_guide(mainGroup = None,  prefix = " ", s = 1): 
    """creating guide for the arm rig. this is only to set locations."""
    if mainGroup is None:
        mainGroup =     cmds.group(em = True, n = prefix + group_name)
    else:
        prefix = cmds.getAttr(mainGroup+'.prefix')
    if not cmds.attributeQuery('prefix', node = mainGroup, exists = True):
        cmds.addAttr(mainGroup, ln = 'prefix', dt = 'string')
        cmds.setAttr(mainGroup + '.prefix', prefix, type = 'string')
    
    #Creatng locators to guide controls 
    
    #creating shoulder locators, changing scale in local spoace and moving it to default position
    shoulder_locator = utilities.addLocator    (name = prefix + shoulder_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [6, 140, 0],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + shoulder_loc_name)

    
    #creating arm locators, changing scale in local spoace and moving it to default position
    arm_locator = utilities.addLocator    (name = prefix + arm_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [12, 140, 0],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + arm_loc_name)

    
    #creating elbow locators, changing scale in local spoace and moving it to default position
    elbow_locator = utilities.addLocator    (name = prefix + elbow_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [24, 140, -5],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + elbow_loc_name)

    
    
    #creating wrist locators, changing scale in local spoace and moving it to default position
    wrist_locator = utilities.addLocator    (name = prefix + wrist_loc_name,
                                            parent = mainGroup,
                                            size = 10, color = None,
                                            translation = [36, 140, 0],  rotation = [0, 0, 0],
                                            mainGroup = mainGroup,
                                            linkToAttr = 'loc_' + wrist_loc_name)

    
    
    #Creating FK controls - these translations and rotations are locked and can be controlled using the locators
    
    shoulder_control = cmds.circle(name = (prefix + shoulder_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    
    arm_control = cmds.circle(name = (prefix + arm_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    
    elbow_control = cmds.circle(name = (prefix + elbow_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    
    wrist_control = cmds.circle(name = (prefix + elbow_control_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    
    #creating IK controls - the user has access to te roation and translation of these
    pole_vector = cmds.curve(d = 1, p = [(0,4,0), (5, -2, 0), (-5, -2, 0), (0, 4, 0)], k = (0, 1, 2, 3), n = prefix + pv_name)
    
    #creating IK handle for arms
    ik_handle = cmds.curve(d = 1, p = [(5, 5, 5), (-5, 5, 5), (5, 5, -5), (-5, 5, -5), (-5, 5, 5), (-5, -5, 5), (5, -5, 5), (5, 5, 5), (5, 5, -5), (5, -5, -5), (5, -5, 5), (-5, -5, 5), (-5, -5, -5), (5, -5, -5), (5, 5, -5), (-5, 5, -5), (-5, -5, -5)], k = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16))

    #creating heirarchy
    cmds.parent(shoulder_control, shoulder_locator)
    cmds.parent(arm_control, arm_locator)
    cmds.parent(elbow_control, elbow_locator)
    cmds.parent(wrist_control, wrist_locator)
    cmds.parent(pole_vector, elbow_control)
    cmds.parent(ik_handle, wrist_control)
    
    #creating FK control heirarchy
    cmds.parent(arm_locator, shoulder_locator)
    cmds.parent(elbow_locator, arm_locator)
    cmds.parent(wrist_locator, elbow_locator)

    #moving the controls to their positions relative to the locators
    cmds.setAttr(shoulder_control + '.translate', 0, 0, 0)
    cmds.setAttr(arm_control + ".translate", 0, 0, 0)
    cmds.setAttr(elbow_control + ".translate", 0, 0, 0)
    cmds.setAttr(wrist_control + ".translate", 0, 0, 0)
    cmds.setAttr(pole_vector + ".translate", 0, -36, 0)
    cmds.setAttr(ik_handle + ".translate", 15, -5, -7)
	
    #setting up aim rotations so the arm always faces the elbow, and the elbow always faces the wrist
    cmds.aimConstraint(wrist_control, elbow_control, worldUpType = "object", worldUpObject = arm_locator, upVector = (0.0, 1.0, 0.0))
    cmds.aimConstraint(elbow_control, arm_control, worldUpType = "object", worldUpObject = wrist_locator, upVector = (0.0, 1.0, 0.0))
    
    #locking and hiding appropriate controls
    cmds.setAttr(arm_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(elbow_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(wrist_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    #YOU WANT THE POSITION OF THE LOCATOR AND THE PV AND IK_HANDLE (note to self)
    
    #creating message attribute to be used in the making of the rig - values passed are the positions of the locators, the IK handle and pole vector
    
    attr_shoulder_guide = '{0}.{1}'.format(mainGroup, shoulder_loc_name)
    cmds.addAttr(mainGroup, longName = shoulder_loc_name, attributeType = 'message')
    cmds.connectAttr(shoulder_control + '.message', attr_shoulder_guide, force = True)
    
    attr_arm_guide = '{0}.{1}'.format(mainGroup, arm_loc_name)
    cmds.addAttr(mainGroup, longName = arm_loc_name, attributeType = 'message')
    cmds.connectAttr(arm_control + '.message', attr_arm_guide, force = True)
    
    attr_elbow_guide = '{0}.{1}'.format(mainGroup, elbow_loc_name)
    cmds.addAttr(mainGroup, longName = elbow_loc_name, attributeType = 'message')
    cmds.connectAttr(elbow_control + '.message', attr_elbow_guide, force = True)
    
    attr_wrist_guide = '{0}.{1}'.format(mainGroup, wrist_loc_name)
    cmds.addAttr(mainGroup, longName = wrist_loc_name, attributeType = 'message')
    cmds.connectAttr(wrist_control + '.message', attr_wrist_guide, force = True)
	
    attr_ik_guide = '{0}.{1}'.format(mainGroup, ik_handle_name)
    cmds.addAttr(mainGroup, longName = ik_handle_name, attributeType = 'message')
    cmds.connectAttr(ik_handle + '.message', attr_ik_guide, force = True)
	
    attr_pv_guide = '{0}.{1}'.format(mainGroup, pv_name)
    cmds.addAttr(mainGroup, longName = pv_name, attributeType = 'message')
    cmds.connectAttr(pole_vector + '.message', attr_pv_guide, force = True)
	
    attr_elbowLoc_guide = '{0}.{1}'.format(mainGroup, 'loc_' + elbow_loc_name)
    cmds.addAttr(mainGroup, longName = 'loc_' + 'left' + elbow_loc_name, attributeType = 'message')
    cmds.connectAttr(elbow_locator + '.message', attr_elbowLoc_guide, force = True)
    
    attr_wristLoc_guide = '{0}.{1}'.format(mainGroup, 'loc_' + wrist_loc_name)
    cmds.addAttr(mainGroup, longName = 'loc_' + 'left' + wrist_loc_name, attributeType = 'message')
    cmds.connectAttr(wrist_locator + '.message', attr_wristLoc_guide, force = True)
    
    #accessing the chest control from the spine module to parent the shoulder control to
    parentItem = utilities.getConnectedAnchorItem(mainGroup, 'anchor_guide_chest')
    if parentItem:cmds.parent(shoulder_locator, parentItem)
    
    

def hookup_symmetry(mainGroup, symmetryGroup):
    """replicating left arm guide, shifting it to the right and symmetry constraining it"""
    
    for name in ['.loc_' + arm_loc_name,
                 '.loc_' + elbow_loc_name,
                 '.loc_' + wrist_loc_name,
                 '.' + ik_handle_name,
                 '.' + pv_name,
                 '.loc_' + shoulder_loc_name]:

        master = cmds.listConnections(symmetryGroup + name, source = True)[0]
        target = cmds.listConnections(mainGroup + name, source = True)[0]
        utilities.createSymmetryConstraint(master, target,  position = True, orientation = True)


    
    




#RIG CREATOR FUNCTION
def build_rig (mainGroup, s = 1): 
    """THIS FUNCTION CREATES THE RIG ON THE BASIS OF THE GUIDE POSITIONS"""

    #gets the prefix from the extra attribites of the guide group
    prefix = cmds.getAttr(mainGroup + '.prefix')
    
    #this is defined on the basis of the selection 
    mainGroup = mainGroup
    
    #gets the anchors from the spine module so the arm controls can be parent in heirarchy to the rest of the rig
    controlParent = utilities.getConnectedAnchorItem( mainGroup, 'anchor_rig_chest_control' )
    if not controlParent:controlParent = mainGroup
    print "armguide CP >>>", controlParent
        
    weightParent = utilities.getConnectedAnchorItem( mainGroup, 'anchor_rig_chest_weight' )
    if not weightParent:weightParent = mainGroup
    print "armguide WP >>>", weightParent
  
    hiddenRigParent = utilities.getConnectedAnchorItem(mainGroup, 'anchor_hidden_rig')
    if not hiddenRigParent:hiddenRigParent = mainGroup
    print "armguide HRP >>>:", hiddenRigParent
        
    
    #this hides the guide group so it doesn't intefere with the new rig  
    cmds.setAttr(mainGroup + '.visibility', 0)
    
    
    #Finds positions of each control 
    shoulder_location = cmds.listConnections(mainGroup + '.' + shoulder_loc_name, source = True)[0]
    
    arm_location = cmds.listConnections(mainGroup + '.' + arm_loc_name, source = True)[0]
    
    elbow_location = cmds.listConnections(mainGroup + '.' + elbow_loc_name, source = True)[0]
    
    wrist_location = cmds.listConnections(mainGroup + '.' + wrist_loc_name, source = True)[0]
    
    ik_ctrl_location = cmds.listConnections(mainGroup + '.' + ik_handle_name, source = True)[0]
    
    pv_location = cmds.listConnections(mainGroup + '.' + pv_name, source = True)[0]
    
    
    #uses xform to get the world position of each control
    shoulder_translation = cmds.xform(shoulder_location, ws = True, translation = True, query = True) 
    
    shoulder_rotation = cmds.xform(shoulder_location, ws = True, rotation = True, query = True)
    
    arm_translation = cmds.xform(arm_location, ws = True, translation = True, query = True)
    
    arm_rotation = cmds.xform(arm_location, ws = True, rotation = True, query = True)
    
    elbow_translation = cmds.xform(elbow_location, ws = True, translation = True, query = True)
    
    elbow_rotation = cmds.xform(elbow_location, ws = True, rotation = True, query = True)
    
    wrist_translation = cmds.xform(wrist_location, ws = True, translation = True, query = True)
    
    wrist_rotation = cmds.xform(wrist_location, ws = True, rotation = True, query = True)
    
    ik_translation = cmds.xform(ik_ctrl_location, ws = True, translation = True, query = True)
    
    ik_rotation = cmds.xform(ik_ctrl_location, ws = True, rotation = True, query = True)
    
    pv_translation = cmds.xform(pv_location, ws = True, translation = True, query = True)
    
    pv_rotation = cmds.xform(pv_location, ws = True, rotation = True, query = True)
    
    
    #Creates controls on the basis of guide positions 
    shoulder_control = cmds.circle(name = (prefix + "shoulder_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(shoulder_control + '.translate', *shoulder_translation)
    cmds.setAttr(shoulder_control + '.rotate', *shoulder_rotation)
	
    arm_control = cmds.circle(name = (prefix + "arm_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    arm_shape = cmds.listRelatives( arm_control, shapes = True, path = True)[0]
    print ">>>>>>>>>>>>>>",arm_shape
    cmds.setAttr(arm_control + '.translate', *arm_translation)
    cmds.setAttr(arm_control + '.rotate', *arm_rotation)
    
    elbow_control = cmds.circle(name = (prefix + "elbow_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(elbow_control + '.translate', *elbow_translation)
    cmds.setAttr(elbow_control + '.rotate', *elbow_rotation)
    
    wrist_control = cmds.circle(name = (prefix + "wrist_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    cmds.setAttr(wrist_control + '.translate', *wrist_translation)
    cmds.setAttr(wrist_control + '.rotate', *wrist_rotation)
    
    size = s*5
    ik_position = p = [(size, size, size), (-size, size, size), (size, size, -size), (-size, size, -size), (-size, size, size), (-size, -size, size), (size, -size, size), (size, size, size), (size, size, -size), (size, -size, -size), (size, -size, size), (-size, -size, size), (-size, -size, -size), (size, -size, -size), (size, size, -size), (-size, size, -size), (-size, -size, -size)]
    
    ik_ctrl = cmds.curve(d = 1, p = ik_position, k = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), n = prefix + "arm_IK_CTRL")
    cmds.setAttr(ik_ctrl + '.translate', *ik_translation)
    cmds.setAttr(ik_ctrl + '.rotate', *ik_rotation)
    
    pv_ctrl = cmds.curve(d = 1, p = [(s*0,s*4,s*0), (s*5, s*-2, s*0), (s*-5, s*-2, s*0), (s*0, s*4, s*0)], k = (0, 1, 2, 3), n = prefix + "arm_pole_vector_CTRL")
    cmds.setAttr(pv_ctrl + '.translate', *pv_translation)
    cmds.setAttr(pv_ctrl + '.rotate', *pv_rotation)
    
    
    #Zeroes out controls 
    arm_rig_group = cmds.group(em = True, n = prefix + "arm_mainGroup")
    shoulder_zero = cmds.group(em = True, n = prefix + "shoulder_CTRL_ZERO")
    arm_zero = cmds.group(em = True, n = prefix + "arm_CTRL_ZERO")
    elbow_zero = cmds.group(em = True, n = prefix + "elbow_CTRL_ZERO")
    wrist_zero = cmds.group(em = True, n = prefix + "wrist_CTRL_ZERO")
    ik_zero = cmds.group(em = True, n = prefix + "IK_CTRL_ZERO")
    pv_zero = cmds.group(em = True, n = prefix + "PV_CTRL_ZERO")
   
    #creates heirarchy for arm rig
    cmds.parent(arm_rig_group, controlParent)
    cmds.matchTransform(shoulder_zero, shoulder_control)
    cmds.matchTransform(arm_zero, arm_control)
    cmds.matchTransform(elbow_zero, elbow_control)
    cmds.matchTransform(wrist_zero, wrist_control) 
    cmds.matchTransform(ik_zero, ik_ctrl)
    cmds.matchTransform(pv_zero, pv_ctrl)
    
    cmds.parent(shoulder_control, shoulder_zero)
    cmds.parent(arm_control, arm_zero)
    cmds.parent(elbow_control, elbow_zero)
    cmds.parent(wrist_control, wrist_zero)
    cmds.parent(ik_ctrl, ik_zero)
    cmds.parent(pv_ctrl, pv_zero)
    
    cmds.parent(shoulder_zero, arm_rig_group)
    cmds.parent(arm_zero, shoulder_control)
    cmds.parent(elbow_zero, arm_control)
    cmds.parent(wrist_zero, elbow_control)
    cmds.parent(ik_zero, arm_rig_group)
    cmds.parent(pv_zero, arm_rig_group)
    
    
    #Creates IK joints and positions them 
    arm_jt = cmds.joint(p = (0, 10, 0), n = prefix + "arm_IK_jt")
    
    elbow_jt = cmds.joint(p = (0, 5, 0), n = prefix + "elbow_IK_jt")
    
    wrist_jt = cmds.joint(p = (0, 0, 0), n = prefix + "wrist_IK_jt")
        
    cmds.parent(arm_jt, w = True)	
    
    #positions IK joints
    cmds.matchTransform(arm_jt, arm_control)
    cmds.matchTransform(elbow_jt, elbow_control)
    cmds.matchTransform(wrist_jt, wrist_control)
    
    cmds.setAttr(elbow_jt + '.preferredAngleZ', cmds.getAttr(elbow_jt + '.rotateZ'))
        
        
    #sets preferred angle so the joints dont snap when the handle is created 

    # cmds.joint(prefix + "arm_IK_jt", e = True, spa = True)
    # cmds.joint(prefix + "elbow_IK_jt", e = True, spa = True) 
    # cmds.joint(prefix + "wrist_IK_jt", e = True, spa = True)
    
    
    #Creates IK Handle for IK joints 
    ik_handle = cmds.ikHandle(n = prefix + "arm_ikhandle", sj = arm_jt, ee = wrist_jt) 
    
    cmds.parent(ik_handle[0], ik_ctrl)
    
   #Creates pole vector control 
    pole_vector = cmds.poleVectorConstraint(pv_ctrl, prefix + "arm_ikhandle") 
    
    cmds.select(clear = True)
    
    
    #Creates weighting joints and positions them 
    shoulder_wt = cmds.joint(p = (0, 15, 0), n = prefix + "shoulder_wt")
    
    arm_wt = cmds.joint(p = (0, 10, 0), n = prefix + "arm_wt")
    
    elbow_wt = cmds.joint(p = (0, 5, 0), n = prefix + "elbow_wt")
    
    wrist_wt = cmds.joint(p = (0, 0, 0), n = prefix + "wrist_wt")
    
    cmds.matchTransform(shoulder_wt, shoulder_control)
    cmds.matchTransform(arm_wt, arm_jt)
    cmds.matchTransform(elbow_wt, elbow_jt)
    cmds.matchTransform(wrist_wt, wrist_jt)
    
    
    #Sets preferred angle for weight joints 
    # cmds.joint(arm_wt, e = True, spa = True)
    # cmds.joint(elbow_wt, e = True, spa = True) 
    # cmds.joint(wrist_wt, e = True, spa = True)
    
    cmds.parent(shoulder_wt, weightParent)
    
    #orient constrains wt joints to the ik joints and fk controls, and assigns it to a variable so it can be used to set up attribute connections 
        
    arm_oc = cmds.orientConstraint(arm_jt, arm_wt, weight = 1)
    elbow_oc= cmds.orientConstraint(elbow_jt, elbow_wt, weight = 1)
    wrist_oc = cmds.orientConstraint(wrist_jt, wrist_wt, weight = 1)
    
    arm_oc = cmds.orientConstraint(arm_control, arm_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    elbow_oc = cmds.orientConstraint(elbow_control, elbow_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    wrist_oc = cmds.orientConstraint(wrist_control, wrist_wt, offset = (0.0, 0.0, 0.0), weight = 1)
    
    print arm_oc
    
    
    #Creates option box, adds Fk_Ik attributue and creates a switch by connecting attributes 
    #FK = 0, IK = 1
    
    option_box = cmds.curve(d = 1, p = [(s*0, s*31, s*9), (s*0, s*36, s*0), (s*0, s*26, s*0), (s*0, s*31, s*9)], k = (0, 1, 2, 3), n = prefix + '_arm_option_box')
    
    cmds.addAttr(option_box, ln = "Fk_Ik", at = 'double', min = 0, max = 1, dv = 0)
    cmds.setAttr(option_box + '.Fk_Ik', keyable = True)
    
    cmds.connectAttr(option_box + '.Fk_Ik', arm_oc[0] + "." +  prefix + "arm_IK_jtW0", force = True)
    cmds.connectAttr(option_box + '.Fk_Ik', elbow_oc[0] + "." +  prefix + "elbow_IK_jtW0", force = True)
    cmds.connectAttr(option_box + '.Fk_Ik', wrist_oc[0] + "." +  prefix + "wrist_IK_jtW0", force = True)
    
    
    pma = cmds.shadingNode('plusMinusAverage', asUtility = True)
    
    print pma 



    
    cmds.connectAttr(option_box + '.Fk_Ik', pma + '.input1D[0]')
    cmds.disconnectAttr(option_box + '.Fk_Ik', pma + '.input1D[0]')
    cmds.connectAttr(option_box + '.Fk_Ik', pma + '.input1D[1]')
    cmds.setAttr(pma + '.operation', 2)
    cmds.setAttr(pma + '.input1D[0]', 1)
    
    cmds.connectAttr(pma + '.output1D', arm_oc[0] + "." +  prefix + "arm_CTRLW1", force = True)
    cmds.connectAttr(pma + '.output1D', elbow_oc[0] + "." +  prefix + "elbow_CTRLW1", force = True)
    cmds.connectAttr(pma + '.output1D', wrist_oc[0] + "." +  prefix + "wrist_CTRLW1", force = True)
    
    
    cmds.connectAttr(option_box + '.Fk_Ik', ik_ctrl + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', pv_ctrl + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', arm_jt + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', elbow_jt + '.visibility')
    cmds.connectAttr(option_box + '.Fk_Ik', wrist_jt + '.visibility')
    
    cmds.connectAttr(pma + '.output1D', arm_control + '.visibility')
    cmds.connectAttr(pma + '.output1D', elbow_control + '.visibility')
    cmds.connectAttr(pma + '.output1D', wrist_control + '.visibility')
    
    cmds.parent(arm_jt, hiddenRigParent)
    cmds.parent(option_box, controlParent)
    
    cmds.parentConstraint(shoulder_control, shoulder_wt, maintainOffset = False, weight = 1)
    
    #Locks and hides unnessecary attributes 
    
    cmds.setAttr(shoulder_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(shoulder_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(shoulder_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(shoulder_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(shoulder_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(shoulder_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(shoulder_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(arm_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(arm_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(elbow_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(elbow_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
    
    cmds.setAttr(wrist_control + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(wrist_control + '.visibility', lock = True, keyable = False, channelBox = False)
    
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
    
    
    cmds.parentConstraint(wrist_wt, option_box, weight = 1)
    
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
    
    cmds.setAttr(ik_handle[0] + '.visibility', 0)
    
    FK_colour = utilities.addColorAttr(option_box, "FK_Colour", red = 1, green = 0, blue = 0)
    IK_colour = utilities.addColorAttr(option_box, "IK_Colour", red = 0, green = 1, blue = 0)
    main_colour = utilities.addColorAttr(option_box, "Main_Colour", red = 0, green = 0, blue = 1)
    
    
    utilities.attachColourToShape(FK_colour, arm_control)
    utilities.attachColourToShape(FK_colour, elbow_control)
    utilities.attachColourToShape(FK_colour, wrist_control)
    utilities.attachColourToShape(IK_colour, ik_ctrl)
    utilities.attachColourToShape(IK_colour, pv_ctrl)
    utilities.attachColourToShape(main_colour, option_box)
    
    
    
    

    
    

    
#arm_rig(mainGroup = cmds.ls(selection = True)[0], s = 1)
	
		
	
	
#arm_wt_orientConstraint1.arm_IK_jtW0
	
#[[u'arm_wt_orientConstraint1'], [u'arm_wt_orientConstraint1']]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
