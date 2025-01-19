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
from DimpleWidget import get_dimple_data

__dir__ = os.path.dirname(__file__)
__iconpath__ = os.path.join(__dir__, 'Dimple.svg')
    
class Dimple:
    """The Dimple feature."""

    def Activated(self):
        """Create a rotated plane and reference line."""
        doc = FreeCAD.ActiveDocument
        # Run a dimple sketch
        # self.duplicate_dimple()
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
        sketch.addConstraint(Sketcher.Constraint('Angle',-1,1,1,1,0.261799))    # Theta
        sketch.addConstraint(Sketcher.Constraint('Distance',2,1,5,0.220902))    # Dimple Depth
        sketch.addConstraint(Sketcher.Constraint('Radius',2,5.08))              # Dimple Radius
        sketch.toggleDriving(12) # Toggle radius to reference dimension
        sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,2,2)) 
        sketch.addConstraint(Sketcher.Constraint('Perpendicular',3,5))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,2,0))
        sketch.addConstraint(Sketcher.Constraint('Distance',5,1,5,2,2.223279))  # Dimple Diameter
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,3,1))
        sketch.renameConstraint(10, u'Theta')
        sketch.renameConstraint(11, u'DimpleDepth')    
        sketch.renameConstraint(12, u'DimpleRadius')  
        sketch.renameConstraint(16, u'DimpleDiameter')  

        # Set default dimple dimensions 
        sketch.setDatum(11,FreeCAD.Units.Quantity('0.203200 mm')) # Dimple Depth    (.008)
        sketch.setDatum(12,FreeCAD.Units.Quantity('7.620000 mm')) # Dimple Radius   (.300)
        sketch.setDatum(16,FreeCAD.Units.Quantity('3.048000 mm')) # Dimple Diameter (.120)

        if sketch.Label == "DimpleSketch001":
            sketch.setDatum(10,FreeCAD.Units.Quantity('0.0 deg'))         # Dimple Theta    (0 degrees)
        else:
            sketch.setDatum(10,FreeCAD.Units.Quantity('9.0 deg'))         # Dimple Theta    (0 degrees)
            print(sketch.Label)

        # Recompute the document
        doc.recompute() 

        # Extract the last three digits from the `Dimple` command name
        dimpleLabel = sketch.Label

        #print(body.Label)
        dimple_number = dimpleLabel[-3:]  # Assumes the last 3 characters are digits

        # Construct the DimpleSketch object name
        sketch_name = f'DimpleSketch{dimple_number}'

        # Construct the body name
        body_name = f'Dimple{dimple_number}'

        # Construct the revolve name
        revolve_name = f'DimpleRevolve{dimple_number}'

        # Construct the Polar Pattern name
        polarPattern_name = f'PolarPattern{dimple_number}'

        # Construct the Z axis name
        Z_Axis_name = f'Z_Axis{dimple_number}'

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

        # Polar Array
        doc.getObject(body_name).newObject('PartDesign::PolarPattern',polarPattern_name)
        doc.getObject(polarPattern_name).Axis = (doc.getObject(Z_Axis_name), [''])
        doc.getObject(polarPattern_name).TransformMode = u"Transform body"
        doc.getObject(polarPattern_name).Reversed = 0
        doc.getObject(polarPattern_name).Mode = 0
        doc.getObject(polarPattern_name).Angle = 360.000000
        doc.getObject(polarPattern_name).Occurrences = 5
        doc.getObject(polarPattern_name).Visibility = True
        doc.getObject(revolve_name).Visibility = False

        if polarPattern_name == "PolarPattern001":
            doc.getObject(polarPattern_name).Occurrences = 1

        # Recompute
        doc.recompute()

        # Set Tip
        doc.getObject(body_name).Tip = doc.getObject(polarPattern_name)
        FreeCADGui.Selection.addSelection('Unnamed',body_name, polarPattern_name)

        # Set the body color
        body.ViewObject.ShapeColor = (0, 204, 162)

        # Make current selected body
        FreeCADGui.Selection.clearSelection()
        FreeCADGui.Selection.addSelection('Unnamed',body_name)

    

    '''
    def duplicate_dimple(self):
        selected_objects = FreeCADGui.Selection.getSelection()

        # Initialize variables with defaults
        diameter = 0.130
        depth = 0.008
        radius = 0.3
        theta = 0
        phi = 45
        array_occurrence = 5
        latest_dimple = None
        highest_number = -1

        # Ensure something is selected
        if selected_objects:
            for obj in selected_objects:
                if obj.TypeId == "PartDesign::Body" and re.match(r"Dimple\d{3}$", obj.Name):
                    # Extract numeric suffix
                    dimple_number = int(obj.Name[-3:])
                    if dimple_number > highest_number:
                        highest_number = dimple_number
                        latest_dimple = obj

        if latest_dimple:
            try:
                dimple_number = latest_dimple.Name[-3:]  # Extract the dimple number as a string
                # Attempt to retrieve dimple data
                diameter, depth, radius, theta, phi, array_occurrence = get_dimple_data(dimple_number)
                print(f"Selected Dimple: {latest_dimple.Name}")
            except Exception as e:
                # Handle failure and use default values
                print(f"Error retrieving dimple data for {latest_dimple.Name}: {e}")
        else:
            print("No dimple body found. Using default values.")

        # Proceed with the rest of your code using the variables
        print(f"Dimple Data - Diameter: {diameter}, Depth: {depth}, Radius: {radius}, Theta: {theta}, Phi: {phi}, Occurrences: {array_occurrence}")


        # Now you can use these variables
        #print(f"Selected Dimple: {dimple_number}")
        print(f"Dimple Diameter: {diameter} inches")
        print(f"Dimple Depth: {depth} inches")
        print(f"Dimple Radius: {radius} inches")
        print(f"Theta: {theta} degrees")
        print(f"Phi: {phi} degrees")
        print(f"Array Occurrence: {array_occurrence}")

        # Set default dimple dimensions 
        sketch.setDatum(10,FreeCAD.Units.Quantity(theta)) # Dimple Theta   
        sketch.setDatum(11,FreeCAD.Units.Quantity(depth)) # Dimple Depth   
        sketch.setDatum(12,FreeCAD.Units.Quantity(radius)) # Dimple Radius  
        sketch.setDatum(16,FreeCAD.Units.Quantity(diameter)) # Dimple Diameter
    '''


    def IsActive(self):
        """Check if the command is active."""
        return bool(FreeCAD.ActiveDocument)


    def GetResources(self):
        """Return resources for the command."""
        return {
            'Pixmap': __iconpath__,
            'MenuText': "Dimple",
            'ToolTip': "Creates a single radius dimple.",
        }
    

FreeCADGui.addCommand('Dimple', Dimple())



