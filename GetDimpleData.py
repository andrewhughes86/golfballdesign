import FreeCAD
import FreeCADGui

doc = FreeCAD.ActiveDocument

def getDimpleNumber():
    """Function to get the label of the currently selected body."""
    selected_object = FreeCADGui.Selection.getSelection()
    DimpleNumner=selected_object[-3:]
    print(selected_object)
    print(f"Dimple Number: {DimpleNumner}")
    

def getDimpleTheta(DimpleNumner):
    Theta = doc.getObject(f"DimpleSketch{DimpleNumner}").getDatum('Theta').Value
    print(f"DimpleSketch{DimpleNumner}")
    print(f"Theta: {Theta}")

def getDimplePhi(DimpleNumner):
    Phi = doc.getObject('DatumPlane').AttachmentOffset = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0.9999999999999999,0,0),0))
    print(f"Phi: {Phi}")



print("End")