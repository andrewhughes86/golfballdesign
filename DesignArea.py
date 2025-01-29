import FreeCAD
import Part
import Sketcher

class DesignArea:
    # Create planes to define the working area for dimples before they are arrayed.

    def Activated(self):
        # Activate
        self.designArea()

   
    def designArea():
        # Define Active Document
        doc = FreeCAD.ActiveDocument

        # Create a new body
        body = doc.addObject('PartDesign::Body', 'DesignArea')

        # Create a new sketch on the specified plane
        sketch = body.addObject("Sketcher::SketchObject", "DesignAreaSketch")

        # Create a new sketch on the specified plane
        sketch = doc.addObject("Sketcher::SketchObject", "DesignAreaSketch")

        # Move sketch under the body
        body.addObject(sketch)

        # Add geometery
        sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 1.0), 22.027790), 1.570796, 3.141593))
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0.0, 22.027790, 0.0),FreeCAD.Vector(-0.0, 0.0, 0.0)))
        sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0.0, -0.0, 0.0),FreeCAD.Vector(-22.027790, 0.0, 0.0)))
    
        # Add constraints
        sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', 0, 1, -2))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', 0, 2, -1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 1, 1, 0, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 0, 3))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 2, 1, 0, 3))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 2, 2, 0, 2))
        
        ### Begin command PartDesign_Revolution
        doc.getObject('Body').newObject('PartDesign::Revolution','DesignArea')
        doc.getObject('DesignArea').Profile = (doc.getObject('DesignAreaSketch'), ['',])
        doc.getObject('DesignArea').ReferenceAxis = (doc.getObject('DesignAreaSketch'),['V_Axis'])
        doc.getObject('DesignArea').Angle = 72.0
        doc.getObject('DesignArea').ViewObject.Selectable = False
        doc.getObject('DesignAreaSketch').Visibility = False
        
        # Recompute
        doc.recompute()

    def IsActive(self):
        """Check if the command is active."""
        return bool(FreeCAD.ActiveDocument)
        