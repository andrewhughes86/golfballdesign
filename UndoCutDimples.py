import FreeCAD
print('start')
bodies = list()
for obj in FreeCAD.ActiveDocument.Objects:
    if obj.isDerivedFrom("PartDesign::Body"):
        # print(obj.Name)
        bodies.append(obj.Name)
print(bodies)
print('end')

doc = FreeCAD.ActiveDocument

# Remove bodies from list
bodies.remove("Dimple001")
bodies.remove("Dimple002")

# Starting variables
cut_prefix = "Cut"  # Prefix for cut objects
cut_index = len(bodies)      

while len(bodies)>0:
    # Get the current dimple to process
    print(f"{cut_prefix}{str(cut_index).zfill(3)}")
    doc.removeObject(f"{cut_prefix}{str(cut_index).zfill(3)}")
    
    #bp.make_cut([base_cut, current_dimple])
    App.ActiveDocument.recompute()
    
    # Increment cut index
    current_dimple = bodies.pop(0)
    cut_index -= 1

doc.removeObject("Cut")

for obj in FreeCAD.ActiveDocument.Objects:
    if obj.isDerivedFrom("PartDesign::Body"):
        doc.getObject(obj.Name).Visibility = True
    
