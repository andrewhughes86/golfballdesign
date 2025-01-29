import FreeCAD
import FreeCADGui
import Part
import Sketcher


def DualRadiusDimple():
    doc = FreeCAD.ActiveDocument
    # Create a sketch on a given plane with a line at a 45-degree angle.
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

    # Draw contruction geometery
    sketch.addGeometry(Part.Circle(FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 21.3995))
    sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(30, 30, 0)))
    sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(20.861796, 4.766982, 0.000000),FreeCAD.Vector(20.230138, 6.616782, 0.000000)))

    # Toggle construction lines
    sketch.toggleConstruction(0) 
    sketch.toggleConstruction(1)
    sketch.toggleConstruction(2)  

    # Create Constraints
    sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,3))
    sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,1,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,0)) 
    sketch.addConstraint(Sketcher.Constraint('Diameter',0,42.799000))
    sketch.setExpression('Constraints[3]', u'<<BallDiameter>>.Diameter')

    # Dual Radius Dimple geometry
    sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(19.925008, 6.516981, 0.0),FreeCAD.Vector(20.339209, 6.652457, 0.0))) 
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 21.399501), 0.224646, 0.316108))
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(23.687599, 23.603011, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 12.322737), 3.922137, 4.040978))
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(16.352345, 14.314296, 0.000000), FreeCAD.Vector(0.000000, 0.000000, 1.000000), 0.488269), 3.968557, 4.506065))

    # Dual Radius Dimple Constraints
    sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,1,2))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',4,1,0))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',3,1,1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,1,2))
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,4,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,2,0))
    sketch.addConstraint(Sketcher.Constraint('Perpendicular',1,2))
    sketch.addConstraint(Sketcher.Constraint('Tangent',6,1,5,2))
    sketch.movePoint(1,2,FreeCAD.Vector(14.816111,15.440909,0),0)
    sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,3,1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,2,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,3,1))
    sketch.addConstraint(Sketcher.Constraint('Equal',4,0))
    
    # Dual Radius Dimple Dimensions
    sketch.addConstraint(Sketcher.Constraint('Distance',2,1,2,2,2.390632))      # Diameter
    sketch.setDatum(16,FreeCAD.Units.Quantity('0.145 in'))                      # Daimeter set to 0.145 in
    sketch.renameConstraint(16, u'DimpleDiameter')
    sketch.addConstraint(Sketcher.Constraint('Distance',3,1,2,0.635705))        # Depth
    sketch.setDatum(17,FreeCAD.Units.Quantity('0.008 in'))                      # Depth set to .008 in
    sketch.renameConstraint(17, u'DimpleDepth')
    sketch.addConstraint(Sketcher.Constraint('Angle',-1,1,1,1,0.261799))        # Theta
    sketch.setDatum(18,FreeCAD.Units.Quantity('45.000000 deg'))                 # Theta set to 45 degrees
    sketch.renameConstraint(18, u'Theta')
    sketch.addConstraint(Sketcher.Constraint('Radius',5,18.873124))             # Radius(maj)
    sketch.setDatum(19,FreeCAD.Units.Quantity('0.800 in'))                      # Radius(maj) set to 0.800
    sketch.renameConstraint(19, u'DimpleRadius')
    sketch.addConstraint(Sketcher.Constraint('Radius',6,1.239549))              # Radius(min)
    sketch.setDatum(20,FreeCAD.Units.Quantity('1.524000 mm'))                   # Radius(min) set to 0.060
    sketch.renameConstraint(20, u'Radius(min)')
    
    if sketch.Label == "DimpleSketch001":
        sketch.setDatum(18,FreeCAD.Units.Quantity('0.0 deg'))                   # Dimple Theta    (0 degrees)
    else:
        sketch.setDatum(18,FreeCAD.Units.Quantity('10.0 deg'))                   # Dimple Theta    (0 degrees)
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