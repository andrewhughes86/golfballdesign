# -*- coding: utf-8 -*-

__title__ = "Golf Ball Design Workbench"
__author__ = "Andy Hughes"
__url__ = ["http://www.freecadweb.org"]
__doc__ = "Golf ball design workbench"
__version__ = "0.0.1"


class GolfBallDesign (Workbench):
    def __init__(self):
        import os
        import GolfBallDesign
        self.__class__.MenuText = "Golf Ball Design"
        self.__class__.ToolTip = "A Golf Ball Design workbench"
        self.__class__.Icon = os.path.join(GolfBallDesign.get_module_path(), "FreeCAD_Logo.svg")

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        # import here all the needed files that create your FreeCAD commands
        from Dimple import Dimple
        from GolfBall import GolfBall
        
        #self.list = ["Dimple"] # A list of command names created in the line above
        self.list = ["GolfBall","Dimple"] # A list of command names created in the line above
        self.appendToolbar("Golf Ball Design", self.list) # creates a new toolbar with your commands
        self.appendMenu("Golf Ball Design", self.list) # creates a new menu

    def Activated(self):
        "This function is executed when the workbench is activated"
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu(self.__class__.MenuText, self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
    
       
Gui.addWorkbench(GolfBallDesign())
