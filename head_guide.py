import maya.cmds as cmds 
import utilities
#HEAD GUIDE AND RIG

neck_ctrl_name = "neck_CTRL_guide"
head_ctrl_name = "head_CTRL_guide"
jaw_ctrl_name = "jaw_CTRL_guide"
neck_locator_name = "neck_locator"
head_locator_name = "head_locator"
jaw_locator_name = "jaw_locator"
group_name = "head_guide_group"



def init_guide(mainGroup = None):

    print "DOING INIT"
    utilities.addAnchor(mainGroup, 'anchor_guide_chest', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_rig_chest_control', targetItem = None)
    utilities.addAnchor(mainGroup, 'anchor_rig_chest_weight', targetItem = None)
    
    utilities.addAnchor(mainGroup, 'anchor_hidden_rig', targetItem = None)
    


def build_guide(mainGroup = None, prefix = " "):
    """guide for buidling a head rig, position values only"""
    
    if mainGroup is None:
        mainGroup = cmds.group(em = True, n = prefix + group_name)
    else:
        prefix = cmds.getAttr(mainGroup+'.prefix')
    if not cmds.attributeQuery('prefix', node = mainGroup, exists = True):
        cmds.addAttr(mainGroup, ln = 'prefix', dt = 'string')
        cmds.setAttr(mainGroup + '.prefix', prefix, type = 'string')


    

    neck_locator = cmds.spaceLocator(n = prefix + neck_locator_name)[0]
    cmds.setAttr(neck_locator + '.localScale', 5, 5, 5)
    cmds.setAttr(neck_locator + '.translate', 0, 153, 2.25)
    head_locator = cmds.spaceLocator(n = prefix + head_locator_name)[0]
    cmds.setAttr(head_locator + '.localScale', 5, 5, 5)
    cmds.setAttr(head_locator + '.translate', 0, 160.8, -1.32)
    jaw_locator = cmds.spaceLocator(n = prefix + jaw_locator_name)[0]
    cmds.setAttr(jaw_locator + '.localScale', 5, 5, 5)
    cmds.setAttr(jaw_locator + '.translate', 0, 164.1, 5.7)
    
    neck_control = cmds.circle(name = (prefix + neck_ctrl_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    head_control = cmds.circle(name = (prefix + head_ctrl_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    jaw_control = cmds.circle(name = (prefix + jaw_ctrl_name), nr = (1,0,0), sw = 360, r = 12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
    
    cmds.parent(neck_control, neck_locator)
    cmds.parent(head_control, head_locator)
    cmds.parent(jaw_control, jaw_locator)
    
    cmds.setAttr(neck_control + '.translate', 0, 0, 0)
    cmds.setAttr(neck_control + '.rotateZ', 90)
    cmds.setAttr(head_control + '.translate', 0, 0, 0)
    cmds.setAttr(head_control + '.rotateZ', 90)
    cmds.setAttr(jaw_control + '.translate', 0, 0, 0)
    cmds.setAttr(jaw_control + '.rotateZ', 90)
    
    
    
    cmds.parent(neck_locator, mainGroup)
    cmds.parent(head_locator, mainGroup)
    cmds.parent(jaw_locator, mainGroup)
    
    cmds.parent(head_locator, neck_locator)
    cmds.parent(jaw_locator, head_locator)
    
    #new//
    cmds.aimConstraint(head_control, neck_control, worldUpType = "vector", worldUpObject = neck_locator, upVector = (0.0, 1.0, 0.0))
    
    cmds.setAttr(neck_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(neck_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(neck_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(head_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(head_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(head_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(jaw_control + ".translateX", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(jaw_control + ".translateY", lock = True, keyable = False, channelBox = False)
    cmds.setAttr(jaw_control + ".translateZ", lock = True, keyable = False, channelBox = False)
    
    attr_group_guide = '{0}.{1}'.format(mainGroup, group_name)
    cmds.addAttr(mainGroup, longName = group_name, attributeType = 'message')
    cmds.connectAttr(mainGroup + '.message', attr_group_guide, force = True)
    
    attr_neck_guide = '{0}.{1}'.format(mainGroup, neck_locator_name)
    cmds.addAttr(mainGroup, longName = neck_locator_name, attributeType = 'message')
    cmds.connectAttr(neck_control + '.message', attr_neck_guide, force = True)
    
    attr_head_guide = '{0}.{1}'.format(mainGroup, head_locator_name)
    cmds.addAttr(mainGroup, longName = head_locator_name, attributeType = 'message')
    cmds.connectAttr(head_control + '.message', attr_head_guide, force = True)
    
    attr_jaw_guide = '{0}.{1}'.format(mainGroup, jaw_locator_name)
    cmds.addAttr(mainGroup, longName = jaw_locator_name, attributeType = 'message')
    cmds.connectAttr(jaw_control + '.message', attr_jaw_guide, force = True)
    
    # utilities.connectAnchor(mainGroup, anchorName = 
    
# connectAnchor( mainGroup, anchorName, targetGroup, targetName):
    #cmds.addAttr(neck_control, longName = "neck_anchor", attributeType = 'message')
    # utilities.addAnchor(mainGroup, 'guide_neck', targetItem = neck_control)
    # utilities.addAnchor( mainGroup, 'anchor_rig_neck_control', targetItem = neck_control)
    # utilities.addAnchor( mainGroup, 'anchor_rig_neck_weight', targetItem = None)
    
    parentItem = utilities.getConnectedAnchorItem(mainGroup, 'anchor_guide_chest')
    print ">>", parentItem
    if parentItem:cmds.parent(neck_locator, parentItem)
    
def hookup_symmetry(mainGroup, symmetryGroup):
    pass
     


def build_rig(mainGroup, s = 1): 

        prefix = cmds.getAttr(mainGroup + '.prefix')
        
        mainGroup = mainGroup 
        
        controlParent = utilities.getConnectedAnchorItem(mainGroup, 'anchor_rig_chest_control')
        if not controlParent:controlParent = mainGroup
        print "headguide CP >>>", controlParent
        
        weightParent = utilities.getConnectedAnchorItem(mainGroup, 'anchor_rig_chest_weight')
        if not weightParent:weightParent = mainGroup
        print "headguide WP >>>", weightParent
        
        hiddenRigParent = utilities.getConnectedAnchorItem(mainGroup, 'anchor_hidden_rig')
        if not hiddenRigParent:hiddenRigParent = mainGroup
        print "headguide HRP >>>:", hiddenRigParent
        
        cmds.setAttr(mainGroup + '.visibility', 0)
        
        neck_location = cmds.listConnections(mainGroup + '.' + neck_locator_name, source = True)[0]
        
        head_location = cmds.listConnections(mainGroup + '.' + head_locator_name, source = True)[0]
        
        jaw_location = cmds.listConnections(mainGroup + '.' + jaw_locator_name, source = True)[0]
        
        
        neck_translation = cmds.xform(neck_location, ws = True, translation = True, query = True)
        neck_rotation = cmds.xform(neck_location, ws = True, rotation = True, query = True)
        
        head_translation = cmds.xform(head_location, ws = True, translation = True, query = True)
        head_rotation = cmds.xform(head_location, ws = True, rotation = True, query = True)
        
        jaw_translation = cmds.xform(jaw_location, ws = True, translation = True, query = True)
        jaw_rotation = cmds.xform(jaw_location, ws = True, rotation = True, query = True)
        
        neck_control = cmds.circle(name = (prefix + "neck_CTRL"), nr = (1,0,0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
        cmds.setAttr(neck_control + '.translate', *neck_translation)
        cmds.setAttr(neck_control + '.rotate', *neck_rotation)
        
        head_control = cmds.circle(name = (prefix + "head_CTRL"), nr = (1, 0, 0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
        cmds.setAttr(head_control + '.translate', *head_translation)
        cmds.setAttr(head_control + '.rotate', *head_rotation)
        
        jaw_control = cmds.circle(name = (prefix + "jaw_CTRL"), nr = (1, 0, 0), sw = 360, r = s*12, d = 3, ut = 0, tol = 0.01, s = 9, ch = 0)[0]
        cmds.setAttr(jaw_control + '.translate', *jaw_translation)
        cmds.setAttr(jaw_control + '.rotate', *jaw_rotation)
        
        neck_rig_group = cmds.group(em = True, n = prefix + "mainGroup")
        neck_zero = cmds.group(em = True, n = prefix + "neck_CTRL_ZERO")
        head_zero = cmds.group(em = True, n = prefix + "head_CTRL_ZERO")
        jaw_zero = cmds.group(em = True, n = prefix + "jaw_CTRL_ZERO")
        
        cmds.matchTransform(neck_zero, neck_control)
        cmds.matchTransform(head_zero, head_control)
        cmds.matchTransform(jaw_zero, jaw_control)
        
        cmds.parent(neck_rig_group, controlParent)
        cmds.parent(neck_zero, neck_rig_group)
        cmds.parent(head_zero, neck_control)
        cmds.parent(jaw_zero, head_control)
        
        cmds.parent(neck_control, neck_zero)
        cmds.parent(head_control, head_zero)
        cmds.parent(jaw_control, jaw_zero)
        
        cmds.select(cl = True)
        
        
        neck_jt = cmds.joint(p = (0, 0, 0), n = prefix + "neck_jt")
        head_jt = cmds.joint(p = (0, 0, 0), n = prefix + "head_jt")
        jaw_jt = cmds.joint(p = (0, 0, 0), n = prefix + "jaw_jt")
        cmds.parent(neck_jt, weightParent)
        
        
        cmds.matchTransform(neck_jt, neck_control)
        cmds.matchTransform(head_jt, head_control)
        cmds.matchTransform(jaw_jt, jaw_control)
        
        
        
        cmds.joint(prefix + "neck_jt", e = True, spa = True)
        cmds.joint(prefix + "head_jt", e = True, spa = True)
        cmds.joint(prefix + "jaw_jt", e = True, spa = True)
        
        cmds.parentConstraint(neck_control, neck_jt, weight = 1)
        cmds.orientConstraint(head_control, head_jt, weight = 1)
        cmds.orientConstraint(jaw_control, jaw_jt, weight = 1)
        
        
        
        
        
        cmds.setAttr(neck_control + '.translateX', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_control + '.translateY', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_control + '.translateZ', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_control + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_control + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_control + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_control + '.visibility', lock = True, keyable = False, channelBox = False)
        
        cmds.setAttr(head_control + '.translateX', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_control + '.translateY', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_control + '.translateZ', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_control + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_control + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_control + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_control + '.visibility', lock = True, keyable = False, channelBox = False)
        
        cmds.setAttr(jaw_control + '.translateX', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_control + '.translateY', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_control + '.translateZ', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_control + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_control + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_control + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_control + '.visibility', lock = True, keyable = False, channelBox = False)
        
        cmds.setAttr(neck_jt + '.translateX', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_jt + '.translateY', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_jt + '.translateZ', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_jt + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_jt + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_jt + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(neck_jt + '.visibility', lock = True, keyable = False, channelBox = False)
        
        cmds.setAttr(head_jt + '.translateX', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_jt + '.translateY', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_jt + '.translateZ', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_jt + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_jt + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_jt + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(head_jt + '.visibility', lock = True, keyable = False, channelBox = False)
        
        cmds.setAttr(jaw_jt + '.translateX', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_jt + '.translateY', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_jt + '.translateZ', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_jt + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_jt + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_jt + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr(jaw_jt + '.visibility', lock = True, keyable = False, channelBox = False)

        
        # cmds.parent(mainGroup, controlParent)
        
        
        
    
#head_rig(mainGroup = cmds.ls(selection = True)[0], s = 1)
    
    
    
    
    
