import maya.cmds as cmds


def createSymmetryConstraint( master, target,  position = True, orientation = True, forceIfLocked = False):
    """Creates a Symmetry Connection Between the MASTER NODE and the TARGET NODE...
    The Target will be mirrored in position and rotation in the X-Axis...
    master  <str>  The Name of the NODE that is controlling the conenction.
    """
    multMatrix = cmds.shadingNode('multMatrix', asUtility = True)
    compMatrix = cmds.shadingNode('composeMatrix', asUtility = True)
    cmds.setAttr(compMatrix + '.inputScaleX', -1)
    cmds.connectAttr(master + '.worldMatrix[0]', multMatrix + '.matrixIn[0]', force = True)
    cmds.connectAttr(compMatrix + '.outputMatrix', multMatrix + '.matrixIn[1]', force = True)
    decMatrix = cmds.shadingNode('decomposeMatrix', asUtility = True)
    cmds.connectAttr(multMatrix + '.matrixSum', decMatrix + '.inputMatrix', force = True)
    if orientation:
        #isLocked = cmds.getAttr(target + '.rotate', locked = True, query = True)
        cmds.connectAttr(decMatrix + '.outputRotate', target + '.rotate', force = True)
        cmds.setAttr(target + '.rotate', lock = True)
        
    if position:
        cmds.connectAttr(decMatrix + '.outputTranslate', target + '.translate', force = True)
        cmds.setAttr(target + '.translate', lock = True)
    cmds.connectAttr(target + '.parentInverseMatrix[0]', multMatrix + '.matrixIn[2]', force = True)
    
    
def addNewRigNode( name, preset, prefix, parentNode, symmetryRigNode = None):
    rigNode = cmds.createNode('transform', name = name)
    rigNode = cmds.parent( rigNode, parentNode)[0]
    cmds.addAttr(rigNode, ln = "Preset", dt = 'string')
    cmds.setAttr(rigNode + '.Preset', preset,type = 'string')
    cmds.addAttr(rigNode, ln = 'prefix', dt = 'string')
    cmds.setAttr(rigNode + '.prefix', prefix, type = 'string')
    cmds.addAttr(rigNode, longName = 'symmetryRig', attributeType = 'message')
    if symmetryRigNode and cmds.objExists(symmetryRigNode):
        cmds.connectAttr(symmetryRigNode + '.message', rigNode + '.symmetryRig', force = True)

    return rigNode
    
    
def addLocator( name, parent = None, size = None, translation = None, rotation = None, color = None, mainGroup = None, linkToAttr = None):
    new_locator = cmds.spaceLocator(n = name)[0]
    if isinstance(size, (int, float)):
        cmds.setAttr(new_locator + ".localScale", size, size, size)
    if parent is not None:
        new_locator = cmds.parent(new_locator, parent)[0]
    if isinstance(translation, list):
        cmds.setAttr(new_locator + '.translate', *translation)
    if isinstance(rotation, list):
        cmds.setAttr(new_locator + '.rotate', *rotation)
    if mainGroup and linkToAttr:
        cmds.addAttr(mainGroup, longName = linkToAttr, attributeType = 'message')
        cmds.connectAttr(new_locator + '.message' , mainGroup + '.' + linkToAttr, force = True)
        
    return new_locator
    
    
def addAnchor(mainGroup, name, targetItem = None, targetAnchor = None ):
    anchor = mainGroup + '.' + name
    if not cmds.attributeQuery(name, node = mainGroup, exists = True):
        cmds.addAttr(mainGroup, longName = name, attributeType = 'message')
    if targetItem:
        if targetAnchor is None:targetAnchor = 'message'
        cmds.connectAttr(targetItem + '.' + targetAnchor , anchor, force = True)
    return anchor


def getConnectedAnchorItem(mainGroup, anchorName):
    result = None
    attr =  mainGroup + '.' + anchorName
    print attr
    if cmds.attributeQuery (anchorName, node = mainGroup, exists = True):
        print "Hello", attr
        connections = cmds.listConnections(attr, source = True, destination = False, plugs = True)
        print ">.....",connections
        if connections: 
            node, attrName = connections[0].split('.')
            if attrName != 'message':
                result = getConnectedAnchorItem( node, attrName)
            else:result = node
    return result
    
    
def addColorAttr (mainGroup, attrName, red = 0, green = 0, blue = 0):
    
    
    cmds.addAttr(mainGroup, longName= attrName, usedAsColor=True, attributeType = 'float3')
    cmds.addAttr(mainGroup, longName= attrName+'R', attributeType='float', parent= attrName)
    cmds.addAttr(mainGroup, longName= attrName+'G', attributeType='float', parent= attrName)
    cmds.addAttr(mainGroup, longName= attrName+'B', attributeType='float', parent= attrName)
    attr = mainGroup + '.' + attrName
    cmds.setAttr(attr, red, green, blue)
    return attr
        

def attachColourToShape(colourAttr, node):
    shapes = cmds.listRelatives(node, shapes =True)
    if shapes:
        shape = shapes[0]
        cmds.setAttr(shape + '.overrideEnabled', 1)
        cmds.setAttr(shape + '.overrideRGBColors', 1)
        cmds.connectAttr(colourAttr, shape + '.overrideColorRGB')
        

        
    
