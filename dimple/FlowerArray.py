# -*- coding: utf-8 -*-
__title__ = "Flower Array"
__author__ = "Andy Hughes"
__license__ = "LGPL 2.1"
__doc__ = "Creates a ball by revolving a half-circle sketch"

import os
import FreeCAD
import FreeCADGui
import Part
import Sketcher

__dir__ = os.path.dirname(__file__)
__iconpath__ = os.path.join(__dir__, 'Dimple.svg')
    
class FlowerArray:

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        doc.recompute()
        
        # Run a dimple sketch
        self.dimpleSketch(doc)


    def flowerArray(self, doc):
        """Array one dimple around another."""
        ### Have user select the dimple they want to array and save as a variable
        petalDimple = "selected body"

        ### Have user select the dimple they want to array around and save as a variable
        centerDimple = "selected body"

        ### Create a datum line that is part of the dimple you want to array that is in the center of the dimple you want array around
        
        # Construct the Revolve name
        revolve_name = f'DimpleRevolve{dimple_number}'
        datumLine_name = f'DatumLine{dimple_number}'

        # Create datum line
        doc.getObject(body_name).newObject('PartDesign::Line',datumLine_name)   
        doc.getObject(datumLine_name).AttachmentSupport = [(doc.getObject(revolve_name),'Face2')]
        doc.getObject(datumLine_name).MapMode = 'AxisOfInertia1'
        doc.recompute()

        ### Run the polar array command using previously defined variables
        doc.getObject('Dimple001').newObject('PartDesign::PolarPattern','PolarPattern')
        doc.getObject('PolarPattern').TransformMode = "Transform body"
        doc.getObject('PolarPattern').Axis = (doc.getObject('DatumLine'), [''])
        doc.getObject('PolarPattern').Angle = 360
        doc.getObject('PolarPattern').Occurrences = 5
        doc.getObject('DimpleRevolve001').Visibility = False
        doc.recompute()


    def IsActive(self):
        """Check if the command is active."""
        return bool(FreeCAD.ActiveDocument)


    def GetResources(self):
        """Return resources for the command."""
        return {
            'Pixmap': __iconpath__,
            'MenuText': "Flower Array",
            'ToolTip': "Creates a dimple array around another dimple.",
        }

FreeCADGui.addCommand('FlowerArray', FlowerArray())