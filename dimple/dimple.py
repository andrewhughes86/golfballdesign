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
        doc.recompute()
        
        # Run a dimple sketch
        self.dimpleSketch(doc)


    def dimpleSketch(self, doc):
        """Create a sketch on a given plane with a line at a 45-degree angle."""

        # Create the body
        dimpleBody = doc.addObject('PartDesign::Body', 'Dimple001')

        # Create a new Datum Plane
        datum_plane = doc.addObject("PartDesign::Plane", "DatumPlane001")
        dimpleBody.Group = dimpleBody.Group + [datum_plane]  # Assign the plane to the body

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

        # Provide visual feedback
        FreeCADGui.ActiveDocument.getObject(datum_plane.Name).Visibility = False

        # Create a new sketch on the specified plane
        sketch = doc.addObject("Sketcher::SketchObject", "DimpleSketch001")
        
        # Move sketch under the body
        dimpleBody.addObject(sketch)

        # Set the support of the sketch to the plane
        sketch.AttachmentSupport = [(datum_plane, '')]
        
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

        # Single Radius Dimple geometry
        sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(23.518042, 7.314624, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 3.680506), 3.360047, 3.906124))
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(19.925008, 6.516981, 0.0),FreeCAD.Vector(20.339209, 6.652457, 0.0)))
        sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 21.399501), 0.224646, 0.316108))
        # Depth Construction Line
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(20.861796, 4.766982, 0.000000),FreeCAD.Vector(20.230138, 6.616782, 0.000000)))

        # Toggle construction
        sketch.toggleConstruction(5) 
        
        # Single Radius Dimple Constraints
        sketch.addConstraint(Sketcher.Constraint('Coincident', 3, 1, 2, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 3, 2, 1, 2))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 3, 0, 3))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 1, 2, 2))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 2, 1, 2))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,1,1))
        sketch.addConstraint(Sketcher.Constraint('Angle',-1,1,1,1,0.261799)) 
        sketch.addConstraint(Sketcher.Constraint('Distance',2,1,5,0.220902))  # Dimple Depth
        sketch.addConstraint(Sketcher.Constraint('Radius',2,5.08)) 
        sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,2,2)) 
        sketch.addConstraint(Sketcher.Constraint('Perpendicular',3,5))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,2,0))
        sketch.addConstraint(Sketcher.Constraint('Distance',5,1,5,2,2.223279)) # Dimple Diameter
        sketch.renameConstraint(10, u'Theta')
        sketch.renameConstraint(11, u'DimpleDepth')    
        sketch.renameConstraint(12, u'DimpleRadius')  
        sketch.renameConstraint(16, u'DimpleDiameter')  

        # Set dimple dimensions 
        sketch.setDatum(11,FreeCAD.Units.Quantity('0.203200 mm')) # Dimple Depth    (.008)
        sketch.setDatum(12,FreeCAD.Units.Quantity('7.620000 mm')) # Dimple Radius   (.300)
        sketch.setDatum(16,FreeCAD.Units.Quantity('3.048000 mm')) # Dimple Diameter (.120)

        # Recompute the document
        doc.recompute() 

        # Extract the last three digits from the `Dimple` command name
        dimpleLabel = sketch.Label

        #print(body.Label)
        dimple_number = dimpleLabel[-3:]  # Assumes the last 3 characters are digits

        # Construct the DimpleSketch object name
        sketch_name = f'DimpleSketch{dimple_number}'
        #print(sketch_name)

        # Construct the body name
        body_name = f'Dimple{dimple_number}'

        # Ensure the sketch is inside the body
        body = doc.getObject(body_name)

        # Add Revolution feature to the body
        revolveDimple = body.newObject('PartDesign::Revolution', 'DimpleRevolve001')
        
        # Set the properties of the Revolution
        revolveDimple.Profile = (doc.getObject(sketch_name), [''])
        revolveDimple.Angle = 360.0
        revolveDimple.ReferenceAxis = (doc.getObject(sketch_name), ['Axis0'])
        revolveDimple.Midplane = False
        revolveDimple.Reversed = False
        revolveDimple.Type = 0  # Specifies the revolution type
        revolveDimple.UpToFace = None

        # Update visibility settings
        doc.getObject('DatumPlane001').Visibility = False
        doc.getObject('DimpleSketch001').Visibility = False

        # Set the body color to purple
        body.ViewObject.ShapeColor = (0.5, 0.0, 0.5) 
        
        # Recompute the document to apply changes
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