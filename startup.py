
App.newDocument()
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
Gui.activeDocument().activeView().viewDefaultOrientation()
### End command Std_New
### Begin command PartDesign_Body
App.activeDocument().addObject('PartDesign::Body','Body')
App.ActiveDocument.getObject('Body').Label = 'Body'
# import PartDesignGui
Gui.activateView('Gui::View3DInventor', True)
# Gui.activeView().setActiveObject('pdbody', App.activeDocument().Body)
# Gui.Selection.clearSelection()
# Gui.Selection.addSelection(App.ActiveDocument.Body)
App.ActiveDocument.recompute()
### End command PartDesign_Body
# Gui.Selection.addSelection('Unnamed','Body')
# Gui.runCommand('Std_OrthographicCamera',1)
### Begin command Std_Workbench
Gui.activateWorkbench("GolfBallDesign")

### End command Std_Workbench
Gui.runCommand('BallDiameter',0)
Gui.Selection.clearSelection()
Gui.runCommand('Dimple',0)
# Macro End: /Users/andyhughes/Library/Application Support/FreeCAD/Macro/startup.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
