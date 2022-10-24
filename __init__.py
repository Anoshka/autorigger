import arm_guide
import head_guide
import leg_guide
import spine_guide
import utilities

import maya.cmds as cmds

def createBipedRig():
    """Sets up guide groups and module connections/anchors so that the guide, and consequently the rig can be built into the structure"""

    print "Create Biped"
    
    #BUILD all the RigNodes
    bipedGroup = cmds.createNode('transform', name = 'BipedGuide')
    spine = utilities.addNewRigNode(name = "Spine", preset = "SpineGuide", prefix = " ", parentNode = bipedGroup)
    head = utilities.addNewRigNode(name = "Head", preset = "HeadGuide", prefix = " ", parentNode = bipedGroup)
    leftLeg = utilities.addNewRigNode(name = "LeftLeg", preset = "LegGuide", prefix = "Left", parentNode = bipedGroup)
    rightLeg = utilities.addNewRigNode(name = "RightLeg", preset = "LegGuide", prefix = "Right", parentNode = bipedGroup, symmetryRigNode = leftLeg)
    leftArm = utilities.addNewRigNode(name = "LeftArm", preset = "ArmGuide", prefix = "Left", parentNode = bipedGroup)
    rightArm = utilities.addNewRigNode(name = "RightArm", preset = "ArmGuide", prefix = "Right", parentNode = bipedGroup, symmetryRigNode = leftArm)
    
    print 1
    #INITIALIZE all the RigNodes
    initBipedRig(bipedGroup = bipedGroup)

    print 2
    #HOOKUP all the Anchors
    
    #GUIDES
    utilities.addAnchor(head, "anchor_guide_chest", spine, "Chest_CTRL")
    utilities.addAnchor(leftLeg, "anchor_guide_hip", spine, "Global_CTRL")
    utilities.addAnchor(rightLeg, "anchor_guide_hip", spine, "Global_CTRL")
    utilities.addAnchor(leftArm, "anchor_guide_chest", spine, "Chest_CTRL")
    utilities.addAnchor(rightArm, "anchor_guide_chest", spine, "Chest_CTRL")
    
    #CONTROLS
    utilities.addAnchor(head, "anchor_rig_chest_control", spine, "rig_chest_control")
    utilities.addAnchor(leftLeg, "anchor_rig_hip", spine, "rig_hip_control")
    utilities.addAnchor(rightLeg, "anchor_rig_hip", spine, "rig_hip_control")
    utilities.addAnchor(leftArm, "anchor_rig_chest_control", spine, "rig_spine_control")
    utilities.addAnchor(rightArm, "anchor_rig_chest_control", spine, "rig_spine_control")
    
    #WEIGHTS
    utilities.addAnchor(head, "anchor_rig_chest_weight", spine, "spine_E_wt")
    utilities.addAnchor(leftLeg, "anchor_rig_hip_weight", spine, "spine_A_wt")
    utilities.addAnchor(rightLeg, "anchor_rig_hip_weight", spine, "spine_A_wt")
    utilities.addAnchor(leftArm, "anchor_rig_chest_weight", spine, "rig_spineD_weight")
    utilities.addAnchor(rightArm, "anchor_rig_chest_weight", spine, "rig_spineD_weight")
    
    #HIDDEN 
    utilities.addAnchor(head, "anchor_hidden_rig", spine, "hidden_rig")
    utilities.addAnchor(leftLeg, "anchor_hidden_rig", spine, "hidden_rig")
    utilities.addAnchor(rightLeg, "anchor_hidden_rig", spine, "hidden_rig")
    utilities.addAnchor(leftArm, "anchor_hidden_rig", spine, "hidden_rig")
    utilities.addAnchor(rightArm, "anchor_hidden_rig", spine, "hidden_rig")
    
    return bipedGroup
    

def initBipedRig(bipedGroup = None):
    """Adds presets to supplied group. These presets will help structure the guide and place them into heirarchy"""
    print "INIT_Guide"
    
    #if there is no supplied group, the presets will be added to the selected group
    if bipedGroup is None:
        curSel = cmds.ls(selection = True)
        if curSel:bipedGroup = curSel[0]
        
    #if there is no biped group supplied and no selection, an error will be displayed
    if bipedGroup is None or not cmds.objExists(bipedGroup):
        print "INVALID BIPED GROUP SUPPLIED"
    
    #if a biped group is supplied, presets will be added to supplied group
    else:
        rigNodes = cmds.listRelatives(bipedGroup, children = True, path = True)
        if rigNodes:
            for rigNode in rigNodes:
                if cmds.nodeType(rigNode) != 'transform':
                    continue
                curPreset = cmds.getAttr(rigNode + '.Preset')
                
                rigModule = None
                if curPreset == "LegGuide":
                    rigModule = leg_guide
                elif curPreset == "SpineGuide":
                    rigModule = spine_guide
                elif curPreset == "HeadGuide":
                    rigModule = head_guide
                elif curPreset == "ArmGuide":
                    rigModule = arm_guide
                if rigModule is None:continue

                rigModule.init_guide(rigNode)


def buildBipedGuide(bipedGroup= None):
    """Builds guide into the supplied group structure. This guide will be used to determine the position, rotation and scale of the rig"""
    
    #if there is no supplied biped group, a guide will be created for the selection
    if bipedGroup is None:
        curSel = cmds.ls(selection = True)
        if curSel:bipedGroup = curSel[0]
    
    #if there is no supplied group and no selection, an error will be displayed
    if bipedGroup is None or not cmds.objExists(bipedGroup):
        print "INVALID BIPED GROUP SUPPLIED"
        cmds.error("INVALID BIPED GROUP SUPPLIED")
    
    #if there is a supplied biped group, a biped guide will be built into the structure determined by the group's preset
    else:
        rigNodes = cmds.listRelatives( bipedGroup, children = True, path = True)
        if rigNodes:
            for rigNode in rigNodes:
                if cmds.nodeType(rigNode) != 'transform':
                    continue
                curPreset = cmds.getAttr(rigNode + '.Preset')
                
                rigModule = None
                if curPreset == "LegGuide":
                    rigModule = leg_guide
                elif curPreset == "SpineGuide":
                    rigModule = spine_guide
                elif curPreset == "HeadGuide":
                    rigModule = head_guide
                elif curPreset == "ArmGuide":
                    rigModule = arm_guide
                 
                if rigModule is None:continue
                 
                rigModule.build_guide(rigNode)

                #Check if there is a symmetryNode
                #if there is a symmetry node, a right side will be created and symmetry constrained
                symmetryCheck = cmds.listConnections(rigNode + '.symmetryRig', source = True)
                if symmetryCheck: 
                    print "Hookup Symmetry", rigNode
                    rigModule.hookup_symmetry(rigNode, symmetryCheck[0])
                    
    
def buildBipedRig(bipedGroup= None):
    """creates biped rig based on the positions supplied by the biped guide"""
    
    #if there is no supplied biped guide group, a rig will created for the selection
    if bipedGroup is None:
        curSel = cmds.ls(selection = True)
        if curSel:bipedGroup = curSel[0]
        
    #if there is no supplied biped guide group or selection, and error will be displayed
    if bipedGroup is None or not cmds.objExists(bipedGroup):
        print "INVALID BIPED GROUP SUPPLIED"
        cmds.error("INVALID BIPED GROUP SUPPLIED")
        
    #if there is a supplied biped guide group, a rig will be created for it
    else:
        rigNodes = cmds.listRelatives( bipedGroup, children = True, path = True)
        if rigNodes:
            for rigNode in rigNodes:
                if cmds.nodeType(rigNode) != 'transform':
                    continue
                curPreset = cmds.getAttr(rigNode + '.Preset')
                
                rigModule = None
                if curPreset == "LegGuide":
                    rigModule = leg_guide
                elif curPreset == "SpineGuide":
                    rigModule = spine_guide
                elif curPreset == "HeadGuide":
                    rigModule = head_guide
                elif curPreset == "ArmGuide":
                    rigModule = arm_guide
                
                if rigModule is None:continue
                
                rigModule.build_rig(rigNode)
