from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import PySide2 as QT
import maya.cmds as cmds

##########################################################################################################################
#Loggers are nice way to Log Messages/Errors/Warnings to the UI...
import logging
log = logging.getLogger( 'MyTool' )




##########################################################################################################################
class window_tool (MayaQWidgetDockableMixin, QT.QtWidgets.QMainWindow):
	"""Simple UI Example for Maya.
	MayaQWidgetDockableMixin >> Inherits the Maya Dockable Functionality.
								This does all the Maya C++ Wrapping to ensure Pyside can properly talk with Maya.
	QMainWindow	>>				Inherits the PySide Main Window Functionality."""

	def __init__(self, parent = None):
		"""Initializes the new Window Tool."""
		super(window_tool, self).__init__(parent = parent)

		#Set the CENTRAL/MAIN widget for the UI...
		self.wdgMain = QT.QtWidgets.QWidget(self)
		self.setCentralWidget(self.wdgMain)
		self.setWindowTitle("My Fancy Tool 1.2")

		#Create a Text Input Widget for the UI...
		self.numDuplicates = QT.QtWidgets.QSpinBox( self.wdgMain )
		self.numDuplicates.setToolTip ('Number of Duplicate Items to create')

		#Create a Text Input Widget for the UI...
		self.numRandomX = QT.QtWidgets.QDoubleSpinBox( self.wdgMain )
		self.numRandomX.setRange(-100,100)
		self.numRandomX.setToolTip ('Random X range for duplicate.')
		self.numRandomY = QT.QtWidgets.QDoubleSpinBox( self.wdgMain )
		self.numRandomY.setRange(-100,100)
		self.numRandomY.setToolTip ('Random Y range for duplicate.')
		self.numRandomZ = QT.QtWidgets.QDoubleSpinBox( self.wdgMain )
		self.numRandomZ.setRange(-100,100)
		self.numRandomZ.setToolTip ('Random Z range for duplicate.')

		layTranslateRandom = QT.QtWidgets.QHBoxLayout( )	#No Parent means floating layout... this layout will be added into another one
		layTranslateRandom.addWidget (self.numRandomX )
		layTranslateRandom.addWidget (self.numRandomY )
		layTranslateRandom.addWidget (self.numRandomZ )



		#Create a Button that will Execute a Script
		self.btnDo = QT.QtWidgets.QPushButton('Do', self.wdgMain )
		self.btnDo.setToolTip('Execute the Script')
		self.btnDo.released.connect(self.doTool)					#Connect to the script execution when the button is pressed
		
		
		#Layout the widgets ....
		# -First layout the Label and TextInput horizontally...
		# -Secondly, layout the tool input and the button vertical... with a vertical space between the input and button

		layInput = QT.QtWidgets.QFormLayout( )	# This layout will be placed in the main widget
		layInput.addRow('Duplicate Count', self.numDuplicates)
		layInput.addRow('Random Translate', layTranslateRandom)

		layMain = QT.QtWidgets.QVBoxLayout( self.wdgMain )
		layMain.addLayout(layInput)
		layMain.addStretch()
		layMain.addWidget(self.btnDo)
		

	def doTool( self ):
		"""Executes the Tool.
		This should print out the Text in the Input Screen."""
		#log.info( "Checking... {0}".format(self.numDuplicates.value()  ) )
		doRandomSpawn(count = self.numDuplicates.value(),
						randomX = self.numRandomX.value(),
						randomY = self.numRandomY.value(),
						randomZ = self.numRandomZ.value())



def doRandomSpawn(count, randomX,randomY, randomZ ):
	import maya.cmds as cmds 
	import random as random 

	
	e = cmds.ls(selection = True) 

	for c in range(0,count): 
		
		cmds.select(e[c])
		e.append( cmds.duplicate(e[c])[0] )
		
	cmds.select(e)


	l = cmds.ls(selection = True) 
	num = len(l) 

	cmds.select 

	r = 0 
	xrange = randomX
	yrange = randomY
	zrange = randomZ 


	for r in range (0,num):  
		g = l[r] + '.translateX'
		h = l[r] + '.translateZ' 
		i = l[r] + '.translateY' 
		x = cmds.getAttr(g) 
		y = cmds.getAttr(i)
		z = cmds.getAttr(h)
		m = random.uniform(x - xrange , x + xrange) 
		k = random.uniform(y - yrange, y + yrange) 
		n = random.uniform(z- zrange , z + zrange)
		o = random.uniform(0,360) 
		cmds.select(l[r]) 
		cmds.move(m,k,n) 
		cmds.rotate(0,o,0) 
		r += 1
		

	


##########################################################################################################################
def launchUI():
	window = None
	uiName = 'my_tool'
	
	if uiName in globals() and globals()[uiName].isVisible():
		window = globals()[uiName]
		if window.isVisible():
			window.show()
			window.raise_()
			return None

	nuWindow = window_tool()
	globals()[uiName] = nuWindow
	nuWindow.show (dockable = True, floating = True)
	return window
	
	
