import FreeCAD
print('start')
bodies = list()
for obj in FreeCAD.ActiveDocument.Objects:
    if obj.isDerivedFrom("PartDesign::Body"):
        # print(obj.Name)
        bodies.append(obj.Name)
print(bodies)
print('end')

from BOPTools import BOPFeatures

bp = BOPFeatures.BOPFeatures(App.activeDocument())
bp.make_cut(["GolfBall", "Dimple001", ])
bp.make_cut(["Cut", "Dimple002", ])

# Remove bodies from list
bodies.remove("GolfBall")
bodies.remove("Dimple001")
bodies.remove("Dimple002")
print(f"deleted: {bodies}")

# Starting variables
cut_prefix = "Cut"  # Prefix for cut objects
cut_index = 1       # Initial cut index
dimple_prefix = "Dimple"  # Prefix for dimple objects
dimple_index = 3


while bodies:
    # Get the current dimple to process
    current_dimple = bodies.pop(0)
    
    # Determine the base cut object
    bp = BOPFeatures.BOPFeatures(App.activeDocument())
    # base_cut = f"{cut_prefix}{str(cut_index).zfill(3)}" if cut_index > 1 else "GolfBall"
    bp.make_cut([f"{cut_prefix}{str(cut_index).zfill(3)}", f"{dimple_prefix}{str(dimple_index).zfill(3)}", ])
    
    # Apply the cut operation
    
    #bp.make_cut([base_cut, current_dimple])
    App.ActiveDocument.recompute()
    
    # Increment cut index
    cut_index += 1
    dimple_index += 1


App.ActiveDocument.recompute()