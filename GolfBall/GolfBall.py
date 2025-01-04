# -*- coding: utf-8 -*-
__title__ = "Ball Diameter"
__author__ = "Andy Hughes"
__license__ = "LGPL 2.1"
__doc__ = "Creates a ball by revolving a half-circle sketch"

import os
import FreeCAD
import FreeCADGui
import Part
import Sketcher

from PySide import QtGui

__dir__ = os.path.dirname(__file__)
__iconpath__ = os.path.join(__dir__, 'GolfBall.svg')


class GolfBall:
    """The creat Golf BAll command."""

    def Activated(self):
        """Create or update a ball by revolving a half-circle."""
       
        doc = FreeCAD.ActiveDocument

        # delete body
        for obj in doc.Objects:
            if obj.Name == 'Body':
                doc.removeObject('Body')
                doc.recompute()
                break

        # Create variable for Ball Diameter
        var_set = doc.addObject("App::VarSet", "BallDiameter")
        var_set.addProperty("App::PropertyDistance", "Diameter")  # Property is added to the Base group.
        var_set.Diameter = "1.685 in"
        #var_set.addProperty("App::PropertyString", "MyText", group="SomeGroup", doc="Some tooltip information")
        #var_set.MyText = "Golf Ball Diameter"
        doc.recompute()


        # # Check for an existing revolve feature
        # for obj in doc.Objects:
        #     if obj.Name == "GolfBall":
        #         BallDia = 1.685
        #         new_diameter = self.showInputDialog(BallDia)
        #         doc.getObject('Sketch').setDatum(5,(new_diameter*25.4))
        #         doc.recompute()
        #         FreeCADGui.SendMsgToActiveView("ViewFit")
        #         print("The ball diameter is now " + str(new_diameter)+"in")
        #         break

        # else:
        #     # If no revolve exists, create a new one
        #     diameter = self.showInputDialog(1.685)  # Default diameter
        #     if diameter > 0:
        #         self.createRevolvedBall(doc, diameter)
        diameter = 1.685
        self.createRevolvedBall(doc, diameter)

    def createRevolvedBall(self, doc, diameter):
        """Create Ball"""
        # Create a new body
        body = doc.addObject('PartDesign::Body', 'GolfBall')

        # Create a new sketch attached to the XY plane
        sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
        sketch.MapMode = 'FlatFace'

        # Add a circle to the sketch
        radius = diameter / 2
        circle_index = sketch.addGeometry(Part.Circle(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), radius), False)

        # Trim the circle to make it a half-circle
        line = sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(-radius, 0, 0), FreeCAD.Vector(radius, 0, 0)), False)
        sketch.trim(circle_index, FreeCAD.Vector(0, -radius, 0))  # Trim the circle at the bottom

        # Add dimension
        doc.getObject('Sketch').addConstraint(Sketcher.Constraint('Horizontal',1))
        doc.getObject('Sketch').addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2))
        doc.getObject('Sketch').addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1))
        doc.getObject('Sketch').addConstraint(Sketcher.Constraint('Distance',1,1,1,2,42.799000)) 
        doc.getObject('Sketch').setExpression('Constraints[5]', u'<<BallDiameter>>.Diameter')
        doc.getObject('Sketch').addConstraint(Sketcher.Constraint('PointOnObject',1,1,-1))
        #doc.getObject('Sketch').addConstraint(Sketcher.Constraint('TangentViaPoint',-1,1,1,1))

        # Hide the sketch
        sketch.ViewObject.Visibility = False

        # Change to shadded
        FreeCADGui.runCommand('Std_DrawStyle',5)

        # Revolve the sketch
        revolve = body.newObject('PartDesign::Revolution', 'Ball')
        revolve.Profile = sketch
        revolve.ReferenceAxis = (sketch, 'H_Axis')  # Horizontal axis
        revolve.Angle = 360  # Full revolution

        # Recompute the document
        doc.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def updateRevolvedBall(self, revolve, diameter):
        """Update the diameter of an existing revolve."""
        sketch = revolve.Profile
        if not sketch or not isinstance(sketch, FreeCAD.App.Sketcher.SketchObject):
            FreeCAD.Console.PrintError("No valid sketch found in existing revolve.\n")
            return

        # Update the circle's radius in the sketch
        radius = diameter / 2
        circle = sketch.Geometry[0]
        circle.Radius = radius
        sketch.Geometry[0] = circle

        # Recompute the document
        revolve.Document.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def showInputDialog(self, default_diameter):
        """Show a popup dialog to get the diameter from the user."""
        dialog = QtGui.QInputDialog()
        dialog.setWindowTitle("Set Ball Diameter")
        dialog.setLabelText("Enter the ball diameter:")
        dialog.setInputMode(QtGui.QInputDialog.DoubleInput)
        dialog.setDoubleDecimals(3)
        dialog.setDoubleRange(0.1, 1000.0)  # Adjust range as needed
        dialog.setDoubleValue(default_diameter)

        if dialog.exec_() == QtGui.QDialog.Accepted:
            return dialog.doubleValue()
        else:
            return default_diameter  # Default if user cancels

    def IsActive(self):
        """Check if the command is active."""
        return bool(FreeCAD.ActiveDocument)

    def GetResources(self):
        """Return resources for the command."""
        return {
            'Pixmap': __iconpath__,
            'MenuText': "GolfBall",
            'ToolTip': "Creates or updates a ball by revolving a half-circle sketch.",
        }
        

FreeCADGui.addCommand('GolfBall', GolfBall())
