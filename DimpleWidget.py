from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QDockWidget,
    QToolButton,
)
from PySide2.QtCore import Qt, QTimer
import FreeCADGui


def get_selected_body_label():
    """Function to get the label of the currently selected body."""
    selected_objects = FreeCADGui.Selection.getSelection()
    if selected_objects:
        return selected_objects[0].Label
    return None


class CustomWidget(QWidget):
    def __init__(self, input_text1="", input_text2="", input_text3="",input_text4="",input_text5="", button_width=20):
        super().__init__()

        # Selected body label
        self.selected_body_label = QLabel("Selected Body: None")

        # Input fields
        self.line_edit1 = QLineEdit(input_text1)
        self.line_edit2 = QLineEdit(input_text2)
        self.line_edit3 = QLineEdit(input_text3)
        self.line_edit4 = QLineEdit(input_text4)
        self.line_edit5 = QLineEdit(input_text5)

        # Set properties for input fields
        for line_edit in [self.line_edit1, self.line_edit2, self.line_edit3, self.line_edit4, self.line_edit5]:
            line_edit.setFixedWidth(150)
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
            border-radius: 10px; /* Rounded corners */
            padding: 5px;
        }
        QToolButton:hover {
            background-color: #404040; /* Slightly darker gray on hover */
        }
        QToolButton:pressed {
            background-color: #303030; /* Dark gray when pressed */
        }
        """

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
            movement_buttons.addLayout(row_layout)


        # Layouts for input rows
        layout = QVBoxLayout()
        for lbl, line_edit in [(label1, self.line_edit1), (label2, self.line_edit2), (label3, self.line_edit3), (label4, self.line_edit4),(label5, self.line_edit5)]:
            row_layout = QHBoxLayout()
            row_layout.addWidget(lbl)
            row_layout.addWidget(line_edit)
            layout.addLayout(row_layout)

        # Add widgets to layout
        layout.addWidget(self.selected_body_label)
        layout.addWidget(resolution_label)
        layout.addLayout(button_layout)
        layout.addWidget(movement_label)
        layout.addLayout(movement_buttons)

        # Set layout
        self.setLayout(layout)

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_selected_body)
        self.timer.start(500)

    def update_selected_body(self):
        """Update the selected body label dynamically."""
        selected_label = get_selected_body_label()
        self.selected_body_label.setText({selected_label or 'None'})
        
        # Apply bold and change font size
        self.selected_body_label.setStyleSheet("""
            font-size: 16px;  /* Change text size */
            font-weight: bold;  /* Make text bold */
        """)



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
        self.main_window.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)


# Initialize the window
my_win = MyWindow()
