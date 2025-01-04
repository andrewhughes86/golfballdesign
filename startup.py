# -*- coding: utf-8 -*-

# Macro Begin: /Users/andyhughes/Library/Application Support/FreeCAD/Macro/startup.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import FreeCAD
import PartDesign
import PartDesignGui
import GolfBall
import Dimple

App.newDocument()
doc = App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
Gui.activeDocument().activeView().viewDefaultOrientation()
### End command Std_New
### Begin command PartDesign_Body
App.activeDocument().addObject('PartDesign::Body','Body')
App.ActiveDocument.getObject('Body').Label = 'Body'
# import PartDesignGui
Gui.activateView('Gui::View3DInventor', True)

App.ActiveDocument.recompute()
Gui.activateWorkbench("GolfBallDesign")

### End command Std_Workbench
Gui.runCommand('GolfBall',0)
Gui.Selection.clearSelection()

# Create Dimple 001
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane001').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),0))

# Create Dimple 002
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane002').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),45))

# Create Dimple 003
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane003').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),90))

# Create Dimple 004
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane004').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),135))


# Create Dimple 005
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane005').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),180))


# Create Dimple 006
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane006').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),225))


# Create Dimple 007
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane007').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),270))

# Create Dimple 008
Gui.runCommand('Dimple',0)
FreeCAD.getDocument('Unnamed').getObject('DatumPlane008').AttachmentOffset = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0.9999999999999999,0,0),315))

# Recompute
App.ActiveDocument.recompute()