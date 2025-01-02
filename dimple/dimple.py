# -*- coding: utf-8 -*-
__title__ = "Dimple"
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
    
class Dimple:
    """The Dimple feature."""

    def Activated(self):
        """Create a rotated plane and reference line."""
        doc = FreeCAD.ActiveDocument

        # Create a new Datum Plane
        datum_plane = doc.addObject("PartDesign::Plane", "DatumPlane")
        if datum_plane.Label == "DatumPlane":
            datum_plane.Label = "DatumPlane001"
        datum_plane.AttachmentOffset = FreeCAD.Placement(
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Rotation(0, 0, 45)
        )
        datum_plane.MapReversed = False
        datum_plane.AttachmentSupport = [(doc.getObject('Z_Axis'), '')]
        datum_plane.MapMode = 'ObjectXY'

         # Set plane dimensions
        datum_plane.ResizeMode = u"Manual"
        datum_plane.Length = 60  # Length of the plane
        datum_plane.Width = 60   # Width of the plane
        datum_plane.recompute()

        # Move to Datum Plane Folder
        doc.getObject("Group").addObject(doc.getObject(datum_plane.Name))

        # Provide visual feedback
        FreeCADGui.ActiveDocument.getObject(datum_plane.Name).Visibility = False

        # Create a sketch on the new datum plane
        self.dimpleSketch(doc, datum_plane)

        # Create dimple revolve cut
        #self.dimpleRevolve(doc)


    def dimpleSketch(self, doc, plane):
        """Create a sketch on a given plane with a line at a 45-degree angle."""

        # Activate the body
        #doc.getObject("BallDiameter")
        #body = FreeCAD.ActiveDocument.getObject("BallDiameter")
        #FreeCADGui.ActiveDocument.setEdit(body.Name, 0)

        # Create a new sketch on the specified plane
        sketch = doc.addObject("Sketcher::SketchObject", "DimpleSketch001")
        
        # Set the support of the sketch to the plane
        sketch.AttachmentSupport = [(plane, '')]
        
        # Set the mapping mode
        sketch.MapMode = "FlatFace"

        # Draw the sketch
        """Need global variable for ball diameter then update this circle"""
        sketch.addGeometry(Part.Circle(FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 21.3995))
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(30, 30, 0)))

        # Toggle construction lines
        sketch.toggleConstruction(1) 
        sketch.toggleConstruction(0) 

        # Create Constraints
        sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,3))
        sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,1,1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,0))
        sketch.addConstraint(Sketcher.Constraint('Diameter',0,42.799000))
        sketch.setExpression('Constraints[3]', u'<<BallDiameter>>.Diameter')
        sketch.addConstraint(Sketcher.Constraint('Angle',-1,1,1,1,0.316108)) 

        # Single Radius Dimple geometry
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(23.518042, 7.314624, 0.0),FreeCAD.Vector(20.861795, 4.766982, 0.0)))
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(19.925008, 6.516982, 0.0),FreeCAD.Vector(23.518042, 7.314624, 0.0)))
        sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(23.518042, 7.314624, 0.000000), FreeCAD.Vector(0.000000, 0.000000, 1.000000), 3.680506), 3.360047, 3.906124))
       
        # Single Radius Dimple Constraints
        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 3, 2, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 2, 2, 2))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 1, 3, 1))
        sketch.addConstraint(Sketcher.Constraint('Tangent',3,1))
        sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,2,1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,2,0))
        sketch.addConstraint(Sketcher.Constraint('Distance',3,1,3,2,6.142200)) 
        sketch.addConstraint(Sketcher.Constraint('Distance',2,2,3,1.692432)) 
                
        # Recompute the document
        doc.recompute() 
    
    def dimpleRevolve(self, doc):
        
        revolveCut = doc.getObject('BallDiameter').newObject('PartDesign::Groove', 'Dimple001')

        # Extract the last three digits from the `Dimple` command name
        dimpleLabel = revolveCut.Label
        #print(revolveCut.Label)
        dimple_number = dimpleLabel[-3:]  # Assumes the last 3 characters are digits
        
        # Construct the DimpleSketch object name
        sketch_name = f'DimpleSketch{dimple_number}'
        #print(sketch_name)
        
        # Assign the sketch as the profile for the groove
        doc.getObject(dimpleLabel).Profile = (doc.getObject(sketch_name), ['',])
        doc.getObject(dimpleLabel).ReferenceAxis = (doc.getObject(sketch_name), ['V_Axis'])
        doc.getObject(dimpleLabel).Angle = 360.0
        #doc.getObject(dimpleLabel).Angle2 = 60.000000
        doc.getObject(dimpleLabel).ReferenceAxis = (doc.getObject(sketch_name), ['Axis0'])
        doc.getObject(dimpleLabel).Midplane = 0
        doc.getObject(dimpleLabel).Reversed = 0
        doc.getObject(dimpleLabel).Type = 0
        doc.getObject(dimpleLabel).UpToFace = None
        doc.getObject(dimpleLabel).Visibility = True
        doc.getObject(sketch_name).Visibility = False
        
        # Recompute the document
        doc.recompute() 

    def IsActive(self):
        """Check if the command is active."""
        return bool(FreeCAD.ActiveDocument)

    def GetResources(self):
        """Return resources for the command."""
        return {
            'Pixmap': __iconpath__,
            'MenuText': "Dimple",
            'ToolTip': "Creates a rotated plane and reference line for dimples.",
        }

FreeCADGui.addCommand('Dimple', Dimple())