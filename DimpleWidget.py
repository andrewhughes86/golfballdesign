from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QDockWidget,
    QToolButton,
    QShortcut,
    QPushButton,
    QFrame
)
from PySide2.QtGui import QKeySequence
from PySide2.QtCore import Qt
import FreeCADGui
import FreeCAD
import math
import colorsys

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
    array_occurrence = doc.getObject(f"PolarPattern{dimple_number}").Occurrences
    # If the axis is aligned with the x-axis
    if abs(axis.x - 1.0) < 1e-6 and abs(axis.y) < 1e-6 and abs(axis.z) < 1e-6:
        phi = math.degrees(angle_radians)
    else:
        phi = 0.0  # Fallback if phi calculation fails

    return (diameter, depth, radius, theta, phi, array_occurrence)


class SelectionObserver:
    """Observer class for FreeCAD selection events."""
    def __init__(self, custom_widget):
        self.custom_widget = custom_widget

    def addSelection(self, doc, obj, sub, pnt):
        self.custom_widget.update_selected_body()

    def removeSelection(self, doc, obj, sub):
        self.custom_widget.update_selected_body()

    #def clearSelection(self, doc):
    #    self.custom_widget.update_selected_body()


class CustomWidget(QWidget):
    def __init__(self, input_text1="", input_text2="", input_text3="", input_text4="", input_text5="", input_text6=""):
        super().__init__()

        # Selected body label
        self.selected_body_label = QLabel("Selected Body: None")

        self.setup_shortcuts_for_keys()
        self.selected_resolution = None


        # Theta and Phi movement resolution (degrees) 
        self.values = [0.1, 0.5, 1, 3, 5]
        self.current_index = 2
        self.current_resolution = self.values[self.current_index]
        

        # Widget layout (Selected Dimple at the top)
        layout = QVBoxLayout()
        layout.addWidget(self.selected_body_label)

        # Input fieldsx
        self.line_edit1 = QLineEdit(input_text1)
        self.line_edit2 = QLineEdit(input_text2)
        self.line_edit3 = QLineEdit(input_text3)
        self.line_edit4 = QLineEdit(input_text4)
        self.line_edit5 = QLineEdit(input_text5)
        self.line_edit6 = QLineEdit(input_text6)

        # Set properties for input fields
        for line_edit in [self.line_edit1, self.line_edit2, self.line_edit3, self.line_edit4, self.line_edit5, self.line_edit6]:
            line_edit.setFixedWidth(120)
            line_edit.setAlignment(Qt.AlignRight)

        # Labels for input fields
        label1 = QLabel("Diameter:")
        label2 = QLabel("Depth:")
        label3 = QLabel("Radius:")
        label4 = QLabel("Theta:")
        label5 = QLabel("Phi:")
        label6 = QLabel("Array #:")

        # Buttons
        resolution_label = QLabel("Resolution(deg) <-Q E->")
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
        # Buttons
        self.button_map = {}  # Store button references to connect them later
        for btn_text in ["0.1", "0.5", "1", "3", "5"]:
            button = QToolButton()
            button.setText(btn_text)
            button.setFixedWidth(30)
            button.setStyleSheet(button_style)
            button_layout.addWidget(button)

        global_label = QLabel("Global Settings")
        global_label.setAlignment(Qt.AlignCenter)

        # Add input fields and labels
        for lbl, line_edit in [(label1, self.line_edit1), (label2, self.line_edit2), (label3, self.line_edit3), (label4, self.line_edit4), (label5, self.line_edit5), (label6, self.line_edit6)]:
            row_layout = QHBoxLayout()
            row_layout.addWidget(lbl)
            row_layout.addWidget(line_edit)
            layout.addLayout(row_layout)

        # Create a single toggle button
        toggle_array_button = QPushButton("Hide Arrayed Dimples")
        toggle_array_button.setStyleSheet("""
            QPushButton {
                background-color: #447B98;
                border: 1px solid #303030;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)

        # Default state (hidden)
        self.array_hidden = True

        # Define the toggle functionality
        def toggle_array():
            if self.array_hidden:
                toggle_array_button.setText("Show Arrayed Dimples")
                self.hide_array()  # Call the hide function
            else:
                toggle_array_button.setText("Hide Arrayed Dimples")
                self.show_array()  # Call the show function
            self.array_hidden = not self.array_hidden  # Toggle the state


        # Add single radius dimple
        add_dimple_button = QPushButton("Single Radius Dimple")
        add_dimple_button.setStyleSheet("""
            QPushButton {
                background-color: #447B98;
                border: 1px solid #303030;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)
        #hide_array_button.clicked.connect(self.hide_array)
        #show_array_button.clicked.connect(self.show_array)

        # Connect the button to the toggle function
        toggle_array_button.clicked.connect(toggle_array)

        add_dimple_button.clicked.connect(self.add_dimple_script)

        # Flower array button
        flower_array_button = QPushButton("Create Flower Array")
        flower_array_button.setStyleSheet("""
            QPushButton {
                background-color: #447B98;
                border: 1px solid #303030;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)
        flower_array_button.clicked.connect(self.add_dimple_script)


        # Add a line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: white; height: 1px;")
        

        # Horizontal layout for label and line edit
        array_layout = QHBoxLayout()

        # Global array setting
        global_array_label = QLabel("Polar Array:")
        input_text7=""
        global_array = QLineEdit(input_text7)
        global_array.setFixedWidth(120)
        global_array.setAlignment(Qt.AlignRight)

        # Add label and line edit to the horizontal layout
        array_layout.addWidget(global_array_label)
        array_layout.addWidget(global_array)

        # Add widgets to layout
        layout.addWidget(resolution_label)
        layout.addLayout(button_layout)
        layout.addWidget(add_dimple_button)
        layout.addWidget(flower_array_button)

        # Layout line break
        layout.addWidget(line)

        # Global layout widgets
        layout.addWidget(global_label)
        layout.addLayout(array_layout)
        layout.addWidget(toggle_array_button)
        # layout.addWidget(hide_array_button)
        # layout.addWidget(show_array_button)
        
        # Set layout
        self.setLayout(layout)

        # Connect QLineEdits to update functions
        self.line_edit1.editingFinished.connect(self.update_dimple_data)
        self.line_edit2.editingFinished.connect(self.update_dimple_data)
        self.line_edit3.editingFinished.connect(self.update_dimple_data)
        self.line_edit4.editingFinished.connect(self.update_dimple_data)
        self.line_edit5.editingFinished.connect(self.update_dimple_data)
        self.line_edit6.editingFinished.connect(self.update_dimple_data)
    

    def add_dimple_script(self):
        FreeCADGui.runCommand('Dimple',0)
        #print("Running Dimple Script...")

    def on_resolution_button_click(self):
        """Handles the button click event for resolution buttons."""
        # Get the text of the clicked button
        clicked_button = self.sender()
        clicked_resolution = clicked_button.text()

        # Update the selected_resolution variable
        self.selected_resolution = float(clicked_resolution)  # Store the selected resolution

        # Update the button styles to highlight the selected one
        for btn_text, button in self.button_map.items():
            if btn_text == clicked_resolution:
                # Highlight the selected button
                button.setStyleSheet("""
                    QToolButton {
                        background-color: #006400; /* Green color for selected */
                        border: 1px solid #303030;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 11px;
                    }
                    QToolButton:hover {
                        background-color: #404040;
                    }
                    QToolButton:pressed {
                        background-color: #303030;
                    }
                """)
            else:
                # Reset the other buttons to default style
                button.setStyleSheet("""
                    QToolButton {
                        background-color: #447B98;
                        border: 1px solid #303030;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 11px;
                    }
                    QToolButton:hover {
                        background-color: #404040;
                    }
                    QToolButton:pressed {
                        background-color: #303030;
                    }
                """)

        print(f"Selected resolution: {self.selected_resolution}")

    # Hide arrayed dimples
    def hide_array(self):
        for obj in FreeCAD.ActiveDocument.Objects:
            if obj.isDerivedFrom("PartDesign::Revolution"):
                # print(obj.Name)
                obj.ViewObject.Visibility = True
        FreeCAD.ActiveDocument.recompute()

    # Show arrayed dimples
    def show_array(self):
        for obj in FreeCAD.ActiveDocument.Objects:
            if obj.isDerivedFrom("PartDesign::PolarPattern"):
                # print(obj.Name)
                obj.ViewObject.Visibility = True
        FreeCAD.ActiveDocument.recompute()

    # Increase movement resolution
    def increase_value(self):
        """Move to the next value in the list."""
        if self.current_index < 4:  # Check if not at the first index
            self.current_index = (self.current_index + 1) % len(self.values)
            self.current_resolution = self.values[self.current_index]
        print(f"Current Resolution: {self.current_resolution} degrees")  # Optional debug output

    # Decrease movement resolution
    def decrease_value(self):
        """Move to the previous value in the list."""
        if self.current_index > 0:  # Check if not at the first index
            self.current_index = (self.current_index - 1) % len(self.values)
            self.current_resolution = self.values[self.current_index]
        print(f"Current Resolution: {self.current_resolution} degrees")  # Optional debug output

    # Increase theta
    def increase_theta(self):
        current_theta = float(self.line_edit4.text())
        new_theta = current_theta + self.current_resolution
        self.line_edit4.setText(f"{new_theta:.2f}")
        self.update_dimple_data()
        
    # Decrese theta
    def decrease_theta(self):
        current_theta = float(self.line_edit4.text())
        new_theta = current_theta - self.current_resolution
        self.line_edit4.setText(f"{new_theta:.2f}")
        self.update_dimple_data()
        
    # Increase phi
    def increase_phi(self):
        current_phi = float(self.line_edit5.text())
        new_phi = current_phi + self.current_resolution
        self.line_edit5.setText(f"{new_phi:.2f}")
        self.update_dimple_data()
        
    # Decrese phi
    def decrease_phi(self):
        current_phi = float(self.line_edit5.text())
        new_phi = current_phi - self.current_resolution
        self.line_edit5.setText(f"{new_phi:.2f}")
        self.update_dimple_data()

    # Increase dimple diameter
    def increase_dimple_dia(self):
        current_dia = float(self.line_edit1.text())
        new_dia = current_dia + 0.005
        self.line_edit1.setText(f"{new_dia:.3f}")
        self.update_dimple_data()

    # Decrese dimple diameter
    def decrease_dimple_dia(self):
        current_dia = float(self.line_edit1.text())
        new_dia = current_dia - 0.005
        self.line_edit1.setText(f"{new_dia:.3f}")
        self.update_dimple_data()

    def setup_shortcuts_for_keys(self):
        """Set up keyboard shortcuts for the widget."""
        key_actions = {
            "Q": self.decrease_value,
            "W": self.decrease_theta,
            "E": self.increase_value,
            "F": self.decrease_dimple_dia,
            "R": self.increase_dimple_dia,
            "A": self.decrease_phi,
            "S": self.increase_theta,
            "D": self.increase_phi,
        }

        # Create shortcuts for the widget
        for key, action in key_actions.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(action)            


    def update_selected_body(self):
        """Update the selected body label dynamically."""
        selected_label = get_selected_body_label()
        #print(f"Selected Object: {selected_label}")

        if selected_label == "Ball":
            print("Please selecte a dimple.")
        elif selected_label == "GolfBall":
            print("Please selecte a dimple.")
        elif selected_label == "BallDiameter":
            print("Please selecte a dimple.")
        else: 
            dimple_number = selected_label[-3:]

            # Update the label with the correct body name
            self.selected_body_label.setText(f"Dimple{dimple_number}")
            self.selected_body_label.setAlignment(Qt.AlignCenter)
            print(f"Selected: Dimple{dimple_number}")
            
            # Apply bold and change font size
            self.selected_body_label.setStyleSheet("""
                font-size: 16px;  /* Change text size */
                font-weight: bold;  /* Make text bold */
            """)

            # Get dimple data and populate the fields
            diameter, depth, radius, theta, phi, array_occurrence = get_dimple_data(dimple_number)
            self.line_edit1.setText(f"{diameter:.3f}")
            self.line_edit2.setText(f"{depth:.4f}")
            self.line_edit3.setText(f"{radius:.3f}")
            self.line_edit4.setText(f"{theta:.2f}")
            self.line_edit5.setText(f"{phi:.2f}")
            self.line_edit6.setText(f"{array_occurrence}")
       
        
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
            array_occurrence = int(self.line_edit6.text())

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

            # Update array Occurrence  
            doc.getObject(f"PolarPattern{dimple_number}").Occurrences = (array_occurrence) 

            # Recompute the document to apply changes
            doc.recompute()
            print(f"Dimple{dimple_number} updated successfully.")

            # color test
            global dimple_diameter
            global dimple_depth
            dimple_diameter = diameter
            dimple_depth = depth

            self.calculate_rgb(diameter, depth)
          
        except Exception as e:
            print(f"Error updating dimple data: {e}")


    # Change dimple color by dimaeter and depth
    def calculate_rgb(self, dimple_diameter, dimple_depth):
        # Ensure the main number is within the valid range
        if not (0.050 <= dimple_diameter <= 0.200):
            raise ValueError("DimpleDiameter must be between 0.050 and 0.200")

        # Ensure the brightness factor is within the valid range
        if not (0.005 <= dimple_depth <= 0.015):
            raise ValueError("DimpleDepth must be between 0.005 and 0.015")

        # Normalize the main number to a range of 0 to 1
        normalized_value = (dimple_diameter - 0.050) / (0.200 - 0.050)

        # Map the normalized value to the Hue (0 to 1)
        hue = normalized_value

        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
        rgb_color = (int(r * 255), int(g * 255), int(b * 255))

        # Invert brightness factor so 0.015 is dark and 0.005 is bright
        inverted_brightness = 1 - ((dimple_depth - 0.005) / (0.020 - 0.005))

        # Scale down the RGB values by the inverted brightness
        adjusted_rgb = tuple(int(channel * inverted_brightness) for channel in rgb_color)
        #print("Adjusted RGB:", adjusted_rgb)

        # Get the selected FreeCAD object
        selected_objects = FreeCADGui.Selection.getSelection()
        if not selected_objects:
            raise ValueError("No object selected. Please select an object in FreeCAD.")

        selected_object = selected_objects[0]

        # Set the color to the selected FreeCAD object
        selected_object.ViewObject.ShapeColor = (adjusted_rgb[0] / 255, adjusted_rgb[1] / 255, adjusted_rgb[2] / 255)
        #print("Updated color:", selected_object.ViewObject.ShapeColor)

        return adjusted_rgb
 

class MyDockWidget(QDockWidget):
    def __init__(self):
        super().__init__("Dimple Toolbar")
        self.custom_widget = CustomWidget(
            input_text1="Dimple Diameter",
            input_text2="Dimple Depth",
            input_text3="Dimple Radius",
            input_text4="Theta",
            input_text5="Phi", 
            input_text6="Occurrence" 
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
