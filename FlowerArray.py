""# -*- coding: utf-8 -*-
__title__ = "Flower Array"
__author__ = "Andy Hughes"
__license__ = "LGPL 2.1"
__doc__ = "Creates a ball by revolving a half-circle sketch"

import os
import FreeCAD
from PySide import QtGui, QtCore
import FreeCADGui
import Part
import Sketcher
from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QDockWidget,
    QToolButton,
    QShortcut,
    QPushButton
)

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
        ### Have user select the dimple they want to array(petal) and the dimple to array around(center).
        petalDimple = "selected body"
        centerDimple = "selected body"

        # Widget layout (Selected Dimple at the top)
        layout = QVBoxLayout()
        layout.addWidget(self.selected_body_label)

        # Input fields
        self.line_edit1 = QLineEdit(petalDimple)
        self.line_edit2 = QLineEdit(centerDimple)

        
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




class FlowerArrayWidget(QtGui.QDockWidget):
    def __init__(self):
        super(FlowerArrayWidget, self).__init__()
        
        # Set the title of the dock widget
        self.setWindowTitle("Flower Array")
        
        # Create the main container widget
        container = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        
        # Create input fields
        self.line_edit_1 = QtGui.QLineEdit()
        self.line_edit_1.setPlaceholderText("Dimple to array")
        
        self.line_edit_2 = QtGui.QLineEdit()
        self.line_edit_2.setPlaceholderText("Center dimple")
        
        # Create the submit button
        self.button = QtGui.QPushButton("Array")
        self.button.clicked.connect(self.on_button_click)
        
        # Add widgets to the layout
        layout.addWidget(self.line_edit_1)
        layout.addWidget(self.line_edit_2)
        layout.addWidget(self.button)
        
        # Set layout for the container widget
        container.setLayout(layout)
        
        # Set the main widget of the dockable area
        self.setWidget(container)
    
    def on_button_click(self):
        # Fetch values from the input fields
        value1 = self.line_edit_1.text()
        value2 = self.line_edit_2.text()
        
        # Print to the FreeCAD console
        FreeCAD.Console.PrintMessage(f"First Value: {value1}, Second Value: {value2}\n")
        
        # Clear the fields after submission
        self.line_edit_1.clear()
        self.line_edit_2.clear()

# Function to add the dockable widget to FreeCAD
def create_flower_array():
    # Check if the widget already exists
    for flower_widget in FreeCADGui.getMainWindow().findChildren(QtGui.QDockWidget):
        if flower_widget.windowTitle() == "Flower Array":
            flower_widget.show()
            return
    
    # Create a new dockable widget
    flower_widget = FlowerArrayWidget()
    
    # Add the dock widget to the FreeCAD interface
    FreeCADGui.getMainWindow().addDockWidget(QtCore.Qt.RightDockWidgetArea, flower_widget)

# Run the function to create the dockable widget
create_flower_array()
""