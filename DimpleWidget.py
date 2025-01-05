from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QDockWidget,
    QToolButton,
    QShortcut
)
from PySide2.QtGui import QKeySequence
from PySide2.QtCore import Qt
import FreeCADGui
import FreeCAD
import math

def get_selected_body_label():
    """Function to get the label of the currently selected body."""
    selected_objects = FreeCADGui.Selection.getSelection()
    if selected_objects:
        return selected_objects[0].Label
    return None


def get_dimple_data(dimple_number):
    """Retrieve data for the specified dimple."""
    doc = FreeCAD.ActiveDocument

    # Fetching the required data from FreeCAD
    diameter = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('DimpleDiameter').Value / 25.4  # Convert to inches
    depth = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('DimpleDepth').Value / 25.4  # Convert to inches
    radius = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('DimpleRadius').Value / 25.4  # Convert to inches
    theta = doc.getObject(f"DimpleSketch{dimple_number}").getDatum('Theta').Value
    rotation = doc.getObject(f'DatumPlane{dimple_number}').AttachmentOffset.Rotation
    axis = rotation.Axis
    angle_radians = rotation.Angle
    # If the axis is aligned with the x-axis
    if abs(axis.x - 1.0) < 1e-6 and abs(axis.y) < 1e-6 and abs(axis.z) < 1e-6:
        phi = math.degrees(angle_radians)
    else:
        phi = 0.0  # Fallback if phi calculation fails

    return (diameter, depth, radius, theta, phi)


class SelectionObserver:
    """Observer class for FreeCAD selection events."""
    def __init__(self, custom_widget):
        self.custom_widget = custom_widget

    def addSelection(self, doc, obj, sub, pnt):
        self.custom_widget.update_selected_body()

    def removeSelection(self, doc, obj, sub):
        self.custom_widget.update_selected_body()

    def clearSelection(self, doc):
        self.custom_widget.update_selected_body()


class CustomWidget(QWidget):
    def __init__(self, input_text1="", input_text2="", input_text3="", input_text4="", input_text5=""):
        super().__init__()

        # Selected body label
        self.selected_body_label = QLabel("Selected Body: None")

        self.setup_shortcuts_for_keys()

        # Widget layout (Selected Dimple at the top)
        layout = QVBoxLayout()
        layout.addWidget(self.selected_body_label)

        # Input fields
        self.line_edit1 = QLineEdit(input_text1)
        self.line_edit2 = QLineEdit(input_text2)
        self.line_edit3 = QLineEdit(input_text3)
        self.line_edit4 = QLineEdit(input_text4)
        self.line_edit5 = QLineEdit(input_text5)

        # Set properties for input fields
        for line_edit in [self.line_edit1, self.line_edit2, self.line_edit3, self.line_edit4, self.line_edit5]:
            line_edit.setFixedWidth(120)
            line_edit.setAlignment(Qt.AlignRight)

        # Labels for input fields
        label1 = QLabel("Diameter:")
        label2 = QLabel("Depth:")
        label3 = QLabel("Radius:")
        label4 = QLabel("Theta:")
        label5 = QLabel("Phi:")

        # Buttons
        resolution_label = QLabel("Resolution(deg): (Q,E)")
        button_layout = QHBoxLayout()

        button_style = """
        QToolButton {
            background-color: #447B98;
            border: 1px solid #303030;
            border-radius: 5px; /* Rounded corners */
            padding: 5px;
            font-size: 11px;
        }
        QToolButton:hover {
            background-color: #404040; /* Slightly darker gray on hover */
        }
        QToolButton:pressed {
            background-color: #303030; /* Dark gray when pressed */
        }
        """
        # Button connections for Theta movement
        self.button_map = {}  # Store button references to connect them later
        for btn_text in ["0.1", "0.5", "1", "3", "5", "10"]:
            button = QToolButton()
            button.setText(btn_text)
            button.setFixedWidth(30)
            button.setStyleSheet(button_style)
            button_layout.addWidget(button)

        movement_label = QLabel("Theta:(W,S) Phi(A,D)")
        movement_buttons = QVBoxLayout()
        for btn_row in [["Q", "W", "E"], ["A", "S", "D"]]:
            row_layout = QHBoxLayout()
            for btn_text in btn_row:
                button = QToolButton()
                button.setText(btn_text)
                button.setFixedWidth(30)  # Adjust width if needed
                button.setStyleSheet(button_style)
                row_layout.addWidget(button)
                self.button_map[btn_text] = button  # Add button to button_map

                # Connect "W" and "S" buttons to their functionality
                if btn_text == "W":
                    button.clicked.connect(self.decrease_theta)
                elif btn_text == "S":
                    button.clicked.connect(self.increase_theta)

            movement_buttons.addLayout(row_layout)

        # Add input fields and labels
        for lbl, line_edit in [(label1, self.line_edit1), (label2, self.line_edit2), (label3, self.line_edit3), (label4, self.line_edit4), (label5, self.line_edit5)]:
            row_layout = QHBoxLayout()
            row_layout.addWidget(lbl)
            row_layout.addWidget(line_edit)
            layout.addLayout(row_layout)


        # Add widgets to layout
        layout.addWidget(resolution_label)
        layout.addLayout(button_layout)
        layout.addWidget(movement_label)
        layout.addLayout(movement_buttons)

        # Set layout
        self.setLayout(layout)

        # Connect QLineEdits to update functions
        self.line_edit1.editingFinished.connect(self.update_dimple_data)
        self.line_edit2.editingFinished.connect(self.update_dimple_data)
        self.line_edit3.editingFinished.connect(self.update_dimple_data)
        self.line_edit4.editingFinished.connect(self.update_dimple_data)
        self.line_edit5.editingFinished.connect(self.update_dimple_data)
    
    # Increase theta
    def increase_theta(self):
        current_theta = float(self.line_edit4.text())
        new_theta = current_theta + 1
        self.line_edit4.setText(f"{new_theta:.2f}")
        self.update_dimple_data()
        
    # Decrese theta
    def decrease_theta(self):
        current_theta = float(self.line_edit4.text())
        new_theta = current_theta - 1
        self.line_edit4.setText(f"{new_theta:.2f}")
        self.update_dimple_data()

    # Increase phi
    def increase_phi(self):
        current_phi = float(self.line_edit5.text())
        new_phi = current_phi + 1
        self.line_edit5.setText(f"{new_phi:.2f}")
        self.update_dimple_data()
        
    # Decrese phi
    def decrease_phi(self):
        current_phi = float(self.line_edit5.text())
        new_phi = current_phi - 1
        self.line_edit5.setText(f"{new_phi:.2f}")
        self.update_dimple_data()

    def setup_shortcuts_for_keys(self):
        """Set up keyboard shortcuts for the widget."""
        key_actions = {
            "Q": lambda: print("You pressed Q"),
            "W": self.decrease_theta,
            "E": lambda: print("You pressed E"),
            "A": self.decrease_phi,
            "S": self.increase_theta,
            "D": self.increase_phi,
        }

        # Create shortcuts for the widget
        for key, action in key_actions.items():
            try:
                shortcut = QShortcut(QKeySequence(key), self)  # Attach to self (CustomWidget)
                shortcut.activated.connect(action)
                print(f"Shortcut for '{key}' has been set.")
            except Exception as e:
                print(f"Failed to set shortcut for '{key}': {e}")






    def update_selected_body(self):
        """Update the selected body label dynamically."""
        selected_label = get_selected_body_label()
        
        # Check if selected_label is valid and slice the last 3 digits
        if selected_label and isinstance(selected_label, str):
            dimple_number = selected_label[-3:]
        else:
            # If dimple_number is invalid, set a fallback value and make sure it is a string
            dimple_number = "---"  # You can adjust this based on what you need
        
        # Update the label with the correct body name
        self.selected_body_label.setText(f"Dimple{dimple_number}")
        self.selected_body_label.setAlignment(Qt.AlignCenter)
        
        # Apply bold and change font size
        self.selected_body_label.setStyleSheet("""
            font-size: 16px;  /* Change text size */
            font-weight: bold;  /* Make text bold */
        """)

        # Get dimple data and populate the fields
        diameter, depth, radius, theta, phi = get_dimple_data(dimple_number)
        self.line_edit1.setText(f"{diameter:.3f}")
        self.line_edit2.setText(f"{depth:.4f}")
        self.line_edit3.setText(f"{radius:.3f}")
        self.line_edit4.setText(f"{theta:.2f}")
        self.line_edit5.setText(f"{phi:.2f}")


    def update_dimple_data(self):
        """Update the FreeCAD data whenever any field is modified."""
        doc = FreeCAD.ActiveDocument
        selected_label = get_selected_body_label()
        
        if not selected_label:
            print("No body selected.")
            return

        try:
            # Extract dimple number
            dimple_number = selected_label[-3:]

            # Retrieve the updated data from the text fields
            diameter = float(self.line_edit1.text())
            depth = float(self.line_edit2.text())
            radius = float(self.line_edit3.text())
            theta = float(self.line_edit4.text())
            phi = float(self.line_edit5.text())

            # Get the dimple sketch object
            sketch_obj = doc.getObject(f"DimpleSketch{dimple_number}")
            if not sketch_obj:
                print(f"Error: DimpleSketch{dimple_number} not found.")
                return

            # Update dimensions in FreeCAD (convert to mm)
            sketch_obj.setDatum('DimpleDiameter', FreeCAD.Units.Quantity(f"{diameter * 25.4} mm"))
            sketch_obj.setDatum('DimpleDepth', FreeCAD.Units.Quantity(f"{depth * 25.4} mm"))
            sketch_obj.setDatum('DimpleRadius', FreeCAD.Units.Quantity(f"{radius * 25.4} mm"))
            sketch_obj.setDatum('Theta', FreeCAD.Units.Quantity(f"{theta} deg"))

            # Update rotation for phi
            plane_obj = doc.getObject(f'DatumPlane{dimple_number}')
            if plane_obj:
                rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), phi)
                plane_obj.AttachmentOffset.Rotation = rotation
            else:
                print(f"Warning: DatumPlane{dimple_number} not found. Phi not updated.")

            # Recompute the document to apply changes
            doc.recompute()
            print(f"Dimple{dimple_number} updated successfully.")
        
        except Exception as e:
            print(f"Error updating dimple data: {e}")


class MyDockWidget(QDockWidget):
    def __init__(self):
        super().__init__("Dimple Toolbar")
        self.custom_widget = CustomWidget(
            input_text1="Dimple Diameter",
            input_text2="Dimple Depth",
            input_text3="Dimple Radius",
            input_text4="Theta",
            input_text5="Phi", 
        )
        self.setWidget(self.custom_widget)

class MyWindow:
    def __init__(self):
        self.main_window = FreeCADGui.getMainWindow()
        self.dock_widget = MyDockWidget()
        self.main_window.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        # Attach selection observer
        self.observer = SelectionObserver(self.dock_widget.custom_widget)
        FreeCADGui.Selection.addObserver(self.observer)


# Initialize the window
my_win = MyWindow()
