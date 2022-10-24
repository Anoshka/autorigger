import maya.cmds as cmds 
import utilities
#SPINE GUIDE 

groupname = "SpineRig_Group"
cog_ctrl_name = "Cog_CTRL" 
spine_A_ctrl_name = "Spine_A_CTRL" 
spine_B_ctrl_name = "Spine_B_CTRL" 
spine_C_ctrl_name = "Spine_C_CTRL" 
hip_ctrl_name = "Hip_CTRL" 
hip_offset_ctrl_name = "Hip_Offset_CTRL" 
chest_offset_ctrl_name = "Chest_Offset_CTRL" 
chest_ctrl_name = "Chest_CTRL" 
cog_locator_name = "Cog_Locator" 
hip_locator_name = "Spine_A_Locator"
hip_offset_locator_name = "Spine_B_Locator" 
chest_offset_locator_name = "Spine_C_Locator" 
global_control_name = "Global_CTRL"

def init_guide(mainGroup = None):

    print "DOING INIT"
    #HEAD Anchors
    utilities.addAnchor(mainGroup, 'Chest_CTRL', targetItem = None)
    utilities.addAnchor(mainGroup, 'rig_chest_control', targetItem = None)
    utilities.addAnchor(mainGroup, 'spine_E_wt', targetItem = None)
    #ARM Anchors
    # utilities.addAnchor(mainGroup, "Global_CTRL", targetItem = None)
    #utilities.addAnchor(mainGroup, 'Chest_CTRL', targetItem = None)
    utilities.addAnchor(mainGroup, 'rig_spine_control', targetItem = None)
    utilities.addAnchor(mainGroup, 'rig_spineD_weight', targetItem = None)
    #LEG Anchors
    utilities.addAnchor(mainGroup, 'rig_hip_control', targetItem = None)
    utilities.addAnchor(mainGroup, 'Global_CTRL', targetItem = None)
    utilities.addAnchor(mainGroup, 'rig_global_ctrl', targetItem = None) 
    utilities.addAnchor(mainGroup, 'spine_A_wt', targetItem = None)
    #HIDDEN RIG
    utilities.addAnchor(mainGroup, 'hidden_rig', targetItem = None)
    utilities.addAnchor(mainGroup, 'ik_handle', targetItem = None)
    


def build_guide(mainGroup = None, prefix = " ", s = 10): 

    """creating guide for the spine rig. this is only to set locations."""
    if mainGroup is None:
        mainGroup = cmds.group(em = True, n = prefix + groupname)
    else:
        prefix = cmds.getAttr(mainGroup+'.prefix')
    if not cmds.attributeQuery('prefix', node = mainGroup, exists = True):
        cmds.addAttr(mainGroup, ln = 'prefix', dt = 'string')
        cmds.setAttr(mainGroup + '.prefix', prefix, type = 'string')

    print "BUILD GUIDE", prefix

    outSpineDict = {} 
    cog_ctrl =  cmds.curve(d = 1, p = [(-4*s, 0, -4*s), (4*s, 0, -4*s), (4*s, 0, 4*s), (-4*s, 0, 4*s), (-4*s, 0, -4*s)], k = (0, 1, 2, 3, 4),n = prefix + "_" + cog_ctrl_name) 
    spine_A_ctrl = cmds.circle(c = (0, 0, 0), nr = (1, 0, 0), sw = 360, r = s*2, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1, n = prefix + "_" + spine_A_ctrl_name)[0]
    spine_B_ctrl = cmds.circle(c = (0, 0, 0), nr = (1, 0, 0), sw = 360, r = s*2, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1, n = prefix + "_" + spine_B_ctrl_name)[0]
    cmds.move(2, y = True) 
    spine_C_ctrl = cmds.circle(c = (0, 0, 0), nr = (1, 0, 0), sw = 360, r = s*2, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1, n = prefix + "_" + spine_C_ctrl_name)[0]
    cmds.move(4, y = True) 
    
    global_ctrl = cmds.curve(d = 1, p = [(-6*s, 0, -6*s), (6*s, 0, -6*s), (6*s, 0, 6*s), (-6*s, 0, 6*s), (-6*s, 0, -6*s)], k = (0, 1, 2, 3, 4),n = prefix + "_" + global_control_name) 
    
    triPoints = [(0, 2*s, 0), (0, -2*s, -2*s), (0, -2*s, 2*s), (0, 2*s, 0)]
    
    hip_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = prefix + "_" + hip_ctrl_name)
    hip_offset_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = prefix + "_" + hip_offset_ctrl_name)
    cmds.move(2, y = True)
    chest_offset_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = prefix + "_" + chest_offset_ctrl_name)
    cmds.move(4, y = True)
    chest_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = prefix + "_" + chest_ctrl_name)
    cmds.move(6, y = True)

		
    cmds.matchTransform(hip_ctrl, cog_ctrl)
    cmds.matchTransform(hip_offset_ctrl, spine_B_ctrl) 
    cmds.matchTransform(chest_offset_ctrl, spine_C_ctrl) 
   

    cog_Locator = cmds.spaceLocator(n = prefix + "_" + cog_locator_name)[0] 
    cmds.setAttr(cog_Locator + "Shape.localPositionY", -2)
    hip_locator = cmds.spaceLocator(n = prefix + "_" + hip_locator_name)[0] 
    cmds.matchTransform(hip_locator, hip_ctrl)
    hip_offset_locator = cmds.spaceLocator(n = prefix + "_" + hip_offset_locator_name)[0]
    cmds.matchTransform(hip_offset_locator, hip_offset_ctrl)
    chest_offset_locator = cmds.spaceLocator(n = prefix + "_" + chest_offset_locator_name)[0]
    cmds.matchTransform(chest_offset_locator, chest_offset_ctrl)
    
    
    cmds.setAttr(spine_A_ctrl + ".rotateZ", 90)
    cmds.setAttr(spine_B_ctrl + ".rotateZ", 90)
    cmds.setAttr(spine_C_ctrl + ".rotateZ", 90)
    cmds.setAttr(hip_ctrl + ".rotateZ", 90)
    cmds.setAttr(hip_offset_ctrl + ".rotateZ", 90)
    cmds.setAttr(chest_offset_ctrl + ".rotateZ", 90)
    cmds.setAttr(chest_ctrl + ".rotateZ", 90)
    
    cmds.parent(cog_Locator, global_ctrl)
    cmds.parent(cog_ctrl, cog_Locator)
    cmds.parent(hip_locator, cog_ctrl) 
    cmds.parent(spine_A_ctrl, hip_locator)
    cmds.parent(hip_ctrl, spine_A_ctrl) 
    cmds.parent(hip_offset_locator, hip_ctrl) 
    cmds.parent(spine_B_ctrl, hip_offset_locator) 
    cmds.parent(hip_offset_ctrl, spine_B_ctrl) 
    cmds.parent(chest_offset_locator, hip_offset_ctrl)
    cmds.parent(spine_C_ctrl, chest_offset_locator)
    cmds.parent(chest_offset_ctrl, spine_C_ctrl)
    cmds.parent(chest_ctrl, chest_offset_ctrl)
    
    cmds.setAttr(cog_Locator + ".translateY", 102.456)
    cmds.setAttr(hip_locator + ".translateY", 4.5)
    cmds.setAttr(hip_locator + ".rotateY", 90) 
    #cmds.setAttr(hip_locator + ".rotateX", 90) 
    cmds.setAttr(hip_offset_locator + ".translateX", 8.1)
    cmds.setAttr(hip_offset_locator + ".rotateY", 6) 
    cmds.setAttr(chest_offset_locator + ".translateX", 7.8)
    cmds.setAttr(chest_offset_locator + ".rotateY", -7.2) 
    cmds.setAttr(chest_ctrl + ".translateX", 9.36)
   
    
    values = ['X', 'Y', 'Z']
    
    for x in range (0, 3):
        
        cmds.setAttr(spine_A_ctrl + ".translate" + values[x], lock = True, keyable = False, channelBox = False)
        cmds.setAttr(spine_A_ctrl + ".rotate" + values[x], lock = True, keyable = False, channelBox = False)
        cmds.setAttr(spine_A_ctrl + ".scale" + values[x], lock = True, keyable = False, channelBox = False)
    
        cmds.setAttr(spine_B_ctrl + ".translate" + values[x], lock = True, keyable = False, channelBox = False)
        cmds.setAttr(spine_B_ctrl + ".rotate" + values[x], lock = True, keyable = False, channelBox = False)
        cmds.setAttr(spine_B_ctrl + ".scale" + values[x], lock = True, keyable = False, channelBox = False)
        
        cmds.setAttr(spine_C_ctrl + ".translate" + values[x], lock = True, keyable = False, channelBox = False)
        cmds.setAttr(spine_C_ctrl + ".rotate" + values[x], lock = True, keyable = False, channelBox = False)
        cmds.setAttr(spine_C_ctrl + ".scale" + values[x], lock = True, keyable = False, channelBox = False)
        
    
    
    
    cmds.parent(global_ctrl, mainGroup)
    
    
    
    cmds.select(mainGroup) 
    
    attrCogGuide = '{0}.{1}'.format(mainGroup, cog_locator_name)
    cmds.addAttr(mainGroup, longName= cog_locator_name, attributeType='message' )
    cmds.connectAttr(cog_Locator + '.message', attrCogGuide , force=True) 
    
    attrSpineAGuide = '{0}.{1}'.format(mainGroup, hip_locator_name)
    cmds.addAttr(mainGroup, longName= hip_locator_name, attributeType='message' )
    cmds.connectAttr( hip_locator + '.message', attrSpineAGuide, force = True) 
 
    attrSpineBGuide = '{0}.{1}'.format(mainGroup, hip_offset_locator_name)
    cmds.addAttr(mainGroup, longName= hip_offset_locator_name, attributeType='message')
    cmds.connectAttr( hip_offset_locator + '.message', attrSpineBGuide, force = True) 

    attrSpineCGuide = '{0}.{1}'.format(mainGroup, chest_offset_locator_name)
    cmds.addAttr(mainGroup, longName= chest_offset_locator_name, attributeType='message')
    cmds.connectAttr(chest_offset_locator + '.message', attrSpineCGuide, force = True) 

    attrHipGuide = '{0}.{1}'.format(mainGroup, hip_ctrl_name)
    # cmds.addAttr(mainGroup, longName= hip_ctrl_name, attributeType='message')
    # cmds.connectAttr( hip_ctrl + '.message', attrHipGuide, force = True) 
    utilities.addAnchor(mainGroup, hip_ctrl_name, targetItem = hip_ctrl)
    
    attrHipOffsetGuide = '{0}.{1}'.format(mainGroup, hip_offset_ctrl_name)
    cmds.addAttr(mainGroup, longName= hip_offset_ctrl_name, attributeType='message')
    cmds.connectAttr( hip_offset_ctrl + '.message', attrHipOffsetGuide, force = True)
    
    attrChestOffsetGuide = '{0}.{1}'.format(mainGroup, chest_offset_ctrl_name)
    cmds.addAttr(mainGroup, longName= chest_offset_ctrl_name, attributeType='message')
    cmds.connectAttr(chest_offset_ctrl + '.message', attrChestOffsetGuide, force = True)
    
    attrChestGuide = '{0}.{1}'.format(mainGroup, chest_ctrl_name)
    # cmds.addAttr(mainGroup, longName= chest_ctrl_name, attributeType='message')
    # cmds.connectAttr(chest_ctrl + '.message', attrChestGuide, force = True)
    utilities.addAnchor(mainGroup, chest_ctrl_name, targetItem = chest_ctrl)
    
    attrGlobalGuide = '{0}.{1}'.format(mainGroup, global_control_name)
    utilities.addAnchor(mainGroup, global_control_name, targetItem = global_ctrl)
    
    attrGroupGuide = '{0}.{1}'.format(mainGroup, groupname)
    cmds.addAttr(mainGroup, longName= groupname, attributeType='message')
    cmds.connectAttr(mainGroup + '.message', attrGroupGuide, force = True)
    
def hookup_symmetry(mainGroup, symmetryGroup):
    pass
     
 
def build_rig(mainGroup, s = 10): 

    hidden_rig = cmds.group(em = True, name = "HIDDEN_RIG")
    
    # cmds.connectAttr(hidden_rig + '.message', mainGroup + '.' + 'hidden_rig', force = True)
    utilities.addAnchor(mainGroup, 'hidden_rig', targetItem = hidden_rig)
    
    Rig_Group = cmds.listConnections(mainGroup + '.' + groupname, source = True)[0]
    print Rig_Group
    
    Global_CTRL = cmds.listConnections(mainGroup + '.' + global_control_name, source = True)
    
    Hip_CTRL = cmds.listConnections(mainGroup + '.' + hip_ctrl_name, source = True)
    print Hip_CTRL
    Hip_offset_CTRL = cmds.listConnections(mainGroup + '.' + hip_offset_ctrl_name, source = True)
    print Hip_offset_CTRL
    Chest_offset_CTRL = cmds.listConnections(mainGroup + '.' + chest_offset_ctrl_name, source = True)
    print Chest_offset_CTRL
    Chest_CTRL = cmds.listConnections(mainGroup + '.' + chest_ctrl_name, source = True)
    print Chest_CTRL
    Cog_Locator = cmds.listConnections(mainGroup + '.' + cog_locator_name, source = True)
    print Cog_Locator
    Hip_Locator = cmds.listConnections(mainGroup + '.' + hip_locator_name, source = True)
    print Hip_Locator
    Hip_offset_Locator = cmds.listConnections(mainGroup + '.' + hip_offset_locator_name, source = True)
    print Hip_offset_Locator
    Chest_offset_Locator = cmds.listConnections(mainGroup + '.' + chest_offset_locator_name, source = True)
    print Chest_offset_Locator
    cmds.setAttr(Rig_Group + ".visibility", 0)
    
    #Glbal control creation and position
    global_ctrl = cmds.curve(d = 1, p = [(-6*s, 0, -6*s), (6*s, 0, -6*s), (6*s, 0, 6*s), (-6*s, 0, 6*s), (-6*s, 0, -6*s)], k = (0, 1, 2, 3, 4),n = global_control_name) 
    cmds.matchTransform(global_ctrl, Global_CTRL)
    
    #Cog control creation, position and zero
    cog_ctrl = cmds.curve(d = 1, p = [(-4*s, 0, -4*s), (4*s, 0, -4*s), (4*s, 0, 4*s), (-4*s, 0, 4*s), (-4*s, 0, -4*s)], k = (0, 1, 2, 3, 4),n ="Cog_CTRL")
    cmds.matchTransform(cog_ctrl, Cog_Locator)
    cog_ctrl_zero = cmds.group(em = True, n = "Cog_CTRL_ZERO")
    cmds.matchTransform(cog_ctrl_zero, cog_ctrl)
    cmds.parent(cog_ctrl, cog_ctrl_zero)
    
    #Spine A control creation, position and zero 
    spine_A_ctrl = cmds.circle(c = (0, 0, 0), nr = (1, 0, 0), sw = 360, r = s*2, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1, n = "Spine_A_CTRL")[0]
    cmds.matchTransform(spine_A_ctrl, Hip_Locator)
    cmds.setAttr("Spine_A_CTRL.rotateX", 0)
    cmds.setAttr("Spine_A_CTRL.rotateY", 0)
    cmds.setAttr("Spine_A_CTRL.rotateZ", 90)
    spine_A_zero = cmds.group(em = True, n = "Spine_A_CTRL_ZERO")
    cmds.matchTransform(spine_A_zero, spine_A_ctrl)
    cmds.parent(spine_A_ctrl, spine_A_zero)
    
    #Spine B control creation, position and zero
    spine_B_ctrl = cmds.circle(c = (0, 0, 0), nr = (1, 0, 0), sw = 360, r = s*2, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1, n = "Spine_B_CTRL")[0]
    cmds.matchTransform(spine_B_ctrl, Hip_offset_Locator)
    cmds.setAttr("Spine_B_CTRL.rotateX", 0)
    cmds.setAttr("Spine_B_CTRL.rotateY", 0)
    cmds.setAttr("Spine_B_CTRL.rotateZ", 90)
    spine_B_zero = cmds.group(em = True, n = "Spine_B_CTRL_ZERO")
    cmds.matchTransform(spine_B_zero, spine_B_ctrl)
    cmds.parent(spine_B_ctrl, spine_B_zero)
    
    #Spine C control creation, position and zero 
    spine_C_ctrl = cmds.circle(c = (0, 0, 0), nr = (1, 0, 0), sw = 360, r = s*2, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1, n = "Spine_C_CTRL")[0]
    cmds.matchTransform(spine_C_ctrl, Chest_offset_Locator)
    cmds.setAttr("Spine_C_CTRL.rotateX", 0)
    cmds.setAttr("Spine_C_CTRL.rotateY", 0)
    cmds.setAttr("Spine_C_CTRL.rotateZ", 90)
    spine_C_zero = cmds.group(em = True, n = "Spine_C_CTRL_ZERO")
    cmds.matchTransform(spine_C_zero, spine_C_ctrl)
    cmds.parent(spine_C_ctrl, spine_C_zero)
    
    
    #IK Controls position
    triPoints = [(0, 2*s, 0), (0, -2*s, -2*s), (0, -2*s, 2*s), (0, 2*s, 0)]
    
    #hip control creation, position and zero 
    hip_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = "Hip_CTRL")
    cmds.matchTransform(hip_ctrl, Hip_CTRL) 
    hip_ctrl_zero = cmds.group(em = True, n = "Hip_CTRL_ZERO")
    cmds.matchTransform(hip_ctrl_zero, hip_ctrl)
    cmds.parent(hip_ctrl, hip_ctrl_zero) 
    
    #hip offset creation, position and zero
    hip_offset_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = "Hip_Offset_CTRL")
    cmds.matchTransform(hip_offset_ctrl, Hip_offset_CTRL)
    hip_offset_ctrl_zero = cmds.group(em = True, n = "Hip_Offset_CTRL_ZERO")
    cmds.matchTransform(hip_offset_ctrl_zero, hip_offset_ctrl)
    cmds.parent(hip_offset_ctrl, hip_offset_ctrl_zero)
    
    #chest offset control creation, position and zero
    chest_offset_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = "Chest_Offset_CTRL")
    cmds.matchTransform(chest_offset_ctrl, Chest_offset_CTRL)
    chest_offset_ctrl_zero = cmds.group(em = True, n = "Chest_Offset_CTRL_ZERO")
    cmds.matchTransform(chest_offset_ctrl_zero, chest_offset_ctrl)
    cmds.parent(chest_offset_ctrl, chest_offset_ctrl_zero)
    
    #chest control creation, position and zero
    chest_ctrl = cmds.curve(d = 1, p = triPoints, k = (0, 1, 2, 3), n = "Chest_CTRL")
    cmds.matchTransform(chest_ctrl, Chest_CTRL)
    chest_ctrl_zero = cmds.group(em = True, n = "Chest_CTRL_ZERO")
    cmds.matchTransform(chest_ctrl_zero, chest_ctrl)
    cmds.parent(chest_ctrl, chest_ctrl_zero)
    utilities.addAnchor(mainGroup, 'rig_chest_control', targetItem = chest_ctrl)
    
    cmds.connectAttr(chest_ctrl + '.message', mainGroup + '.' + 'rig_chest_control', force = True)
    
    
    
    cmds.parent(cog_ctrl_zero, global_ctrl)
    cmds.parent(chest_offset_ctrl_zero, chest_ctrl)
    cmds.parent(hip_offset_ctrl_zero, hip_ctrl)
    cmds.parent(spine_C_zero, spine_B_ctrl)
    cmds.parent(spine_B_zero, spine_A_ctrl)
    cmds.parent(spine_A_zero, cog_ctrl)
    cmds.parent(hip_ctrl_zero, cog_ctrl)
    cmds.parent(chest_ctrl_zero, spine_C_ctrl)
    
    IK_Spline_Curve = cmds.curve(d = 3, p = [(23, 123, 0), (23, 121, 0), (23, 119, 0), (23, 117, 0)], k = (0, 0, 0, 1, 1, 1), n = "IK_Spline_Curve")
    
    hip_decmat = cmds.shadingNode('decomposeMatrix', asUtility =True)
    cmds.connectAttr(hip_ctrl + ".worldMatrix[0]", hip_decmat + ".inputMatrix")
    cmds.connectAttr(hip_decmat + ".outputTranslate", IK_Spline_Curve + ".controlPoints[0]")
    
    hip_offset_decmat = cmds.shadingNode('decomposeMatrix', asUtility =True)
    cmds.connectAttr(hip_offset_ctrl + ".worldMatrix[0]", hip_offset_decmat + ".inputMatrix")
    cmds.connectAttr(hip_offset_decmat + ".outputTranslate", IK_Spline_Curve + ".controlPoints[1]")
    
    chest_offset_decmat = cmds.shadingNode('decomposeMatrix', asUtility =True)
    cmds.connectAttr(chest_offset_ctrl + ".worldMatrix[0]", chest_offset_decmat + ".inputMatrix")
    cmds.connectAttr(chest_offset_decmat + ".outputTranslate", IK_Spline_Curve + ".controlPoints[2]")
    
    chest_decmat = cmds.shadingNode('decomposeMatrix', asUtility =True)
    cmds.connectAttr(chest_ctrl + ".worldMatrix[0]", chest_decmat + ".inputMatrix")
    cmds.connectAttr(chest_decmat + ".outputTranslate", IK_Spline_Curve + ".controlPoints[3]")
    
    jointA = cmds.joint(p = (0, 0, 0), n = "spine_A_wt")
    jointB = cmds.joint(p = (0, 2, 0), n = "spine_B_wt")
    jointC = cmds.joint(p = (0, 4, 0), n = "spine_C_wt")
    jointD = cmds.joint(p = (0, 6, 0), n = "spine_D_wt")
    jointE = cmds.joint(p = (0, 8, 0), n = "spine_E_wt")
    
    cmds.connectAttr(jointE + '.message',  mainGroup + '.spine_E_wt', force = True)
    cmds.connectAttr(jointA + '.message', mainGroup + '.spine_A_wt', force = True)
    cmds.connectAttr(jointD + '.message', mainGroup + '.rig_spineD_weight', force = True)
    
    print "WHAT!!!!",hip_ctrl
    cmds.connectAttr(hip_ctrl + '.message', mainGroup + '.rig_hip_control')
    cmds.connectAttr(global_ctrl + '.message', mainGroup + '.rig_global_ctrl')
    cmds.connectAttr(chest_ctrl + '.message', mainGroup + '.rig_spine_control')
    #cmds.connectAttr(chest_ctrl + '.message', mainGroup + '.rig_chest_control')
    
    
    
    cmds.select(jointA)
    cmds.select(jointE, add = True)
    cmds.select(IK_Spline_Curve, add = True)
    IK_Handle = cmds.ikHandle(sol = 'ikSplineSolver', ccv = False, n = 'spine_IKSpline')
    
    cmds.setAttr(IK_Handle[0] + '.dTwistControlEnable', 1)
    cmds.setAttr(IK_Handle[0] + '.dWorldUpType', 4)
    cmds.connectAttr(hip_ctrl + '.worldMatrix[0]', IK_Handle[0] + '.dWorldUpMatrix')
    cmds.connectAttr(chest_ctrl + '.worldMatrix[0]', IK_Handle[0] + '.dWorldUpMatrixEnd')
    
    ikHandle_curveInfo = cmds.shadingNode('curveInfo', asUtility = True)
    mul_div = cmds.shadingNode('multiplyDivide', asUtility = True)
    cmds.connectAttr(IK_Spline_Curve + '.local', ikHandle_curveInfo + '.inputCurve')
    cmds.connectAttr(ikHandle_curveInfo + '.arcLength', mul_div + '.input1X')
    cmds.setAttr(mul_div + '.operation', 2)
    cmds.setAttr(mul_div + '.input2X', 4)
    cmds.connectAttr(mul_div + '.output', jointA + '.translate', force = True)
    cmds.connectAttr(mul_div + '.output', jointB + '.translate', force = True)
    cmds.connectAttr(mul_div + '.output', jointC + '.translate', force = True)
    cmds.connectAttr(mul_div + '.output', jointD + '.translate', force = True)
    cmds.connectAttr(mul_div + '.output', jointE + '.translate', force = True)
    
    cmds.setAttr(spine_A_ctrl + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_A_ctrl + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_A_ctrl + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_A_ctrl + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_A_ctrl + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_A_ctrl + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_A_ctrl + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(spine_B_ctrl + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_B_ctrl + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_B_ctrl + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_B_ctrl + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_B_ctrl + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_B_ctrl + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_B_ctrl + '.visibility', lock = True, keyable = False, channelBox = False)
    
    cmds.setAttr(spine_C_ctrl + '.translateX', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_C_ctrl + '.translateY', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_C_ctrl + '.translateZ', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_C_ctrl + '.sx', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_C_ctrl + '.sy', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_C_ctrl + '.sz', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(spine_C_ctrl + '.visibility', lock = True, keyable = False, channelBox = False)
    
    
    
    # IK_Colour = utilities.addColorAttr(global_ctrl, "IK_Colour", red = 0, green = 1, blue = 0)
    # main_Colour = utilities.addColorAttr(global_ctrl, "Main_Colour", red = 0, green = 0, blue = 1)
    # FK_Colour = utilities.addColorAttr(global_ctrl, "FK_Colour", red = 1, green = 0, blue = 0)
    
    
    # def fk_colour(node):
        # return utilities.attachColourToShape(FK_Colour, node)
        
    # def ik_colour(node):
        # return utilities.attachColourToShape(IK_Colour, node)
        
    # def main_colour(node):
        # return utilities.attachColourToShape(main_Colour, node)
        
        
   
    cmds.parent(IK_Spline_Curve, hidden_rig)
    # cmds.parent(IK_Handle, hidden_rig)
    #utilities.addAnchor(mainGroup, 'spine_IKSpline', targetItem = IK_Handle)
    cmds.parent('spine_IKSpline', hidden_rig)
    
    weight_group = cmds.group(em = True, n = "WEIGHTS")
    cmds.parent(jointA, weight_group)
    cmds.setAttr(hidden_rig + '.visibility', 0)
    
    CTRL_Group = cmds.group(em = True, n = "CTRL_Group")
    cmds.parent(global_ctrl, CTRL_Group)
#createSpineRig() 

	

	
	
	
	
	
	
	
	
	
	
