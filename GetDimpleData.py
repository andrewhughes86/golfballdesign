import FreeCAD
import FreeCADGui
import time
import math

doc = FreeCAD.ActiveDocument

def getDimpleNumber():
    """Function to get the label of the currently selected body."""
    selected_object = FreeCADGui.Selection.getSelection()
    if not selected_object:
        print("No object selected.")
        return None
    dimple_number = selected_object[0].Label[-3:]
    print(f"Selected Object: {selected_object[0].Label}")
    print(f"Dimple Number: {dimple_number}")
    return dimple_number

def getDimpleDiameter(dimple_number):
    DimpleDia = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('DimpleDiameter').Value
    # Format to 3 decimal places
    print(f"Diameter: {DimpleDia / 25.4:.3f}")

def getDimpleDepth(dimple_number):
    DimpleDepth = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('DimpleDepth').Value
    # Format to 4 decimal places
    print(f"Depth: {DimpleDepth / 25.4:.4f}")

def getDimpleRadius(dimple_number):
    DimpleRadius = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('DimpleRadius').Value
    # Format to 3 decimal places
    print(f"Radius: {DimpleRadius / 25.4:.3f}")

def getDimpleTheta(dimple_number):
    """Get the Theta value of the specified dimple."""
    theta = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('Theta').Value
    # Format to 2 decimal places
    print(f"Theta: {theta:.2f}")

def getDimplePhi(dimple_number):
    """Get the Phi value (rotation about the x-axis in degrees) of the specified dimple."""
    rotation = doc.getObject(f'DatumPlane{dimple_number}').AttachmentOffset.Rotation
    # Extract the rotation vector
    axis = rotation.Axis
    angle_radians = rotation.Angle  # Full rotation angle
    
    # Check if the axis is aligned with the x-axis
    if abs(axis.x - 1.0) < 1e-6 and abs(axis.y) < 1e-6 and abs(axis.z) < 1e-6:
        angle_degrees = math.degrees(angle_radians)
        # Format to 2 decimal places
        print(f"Phi: {angle_degrees:.2f}")
    

# Run the loop for 5 seconds
start_time = time.time()
while time.time() - start_time < .5:
    dimple_number = getDimpleNumber()
    if dimple_number:
        getDimpleDiameter(dimple_number)
        getDimpleDepth(dimple_number)
        getDimpleRadius(dimple_number)
        getDimpleTheta(dimple_number)
        getDimplePhi(dimple_number)
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage

print("Completed 0.5 seconds of monitoring.")