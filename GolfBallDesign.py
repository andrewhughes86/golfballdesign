# -*- coding: utf-8 -*-

import os
import FreeCAD
from importlib import reload

def get_module_path():
    """ Returns the current module path.
    Determines where this file is running from, so works regardless of whether
    the module is installed in the app's module directory or the user's app data folder.
    (The second overrides the first.)
    """
    return os.path.dirname(__file__)

def makeBallDiameter(base = None, green = False):
    '''Python command to create a Dimple.'''
    from BallDiameter import BallDiameter      
    reload(BallDiameter)     # causes FreeCAD to reload BallDiameter.py every time a new Ball is created. Useful while developping the feature.      
    fp = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "BallDiameter")
    BallDiameter.BallDiameterWorker(fp, base, green)
    vp = BallDiameter.BallDiameterViewProvider(fp.ViewObject)
    FreeCAD.ActiveDocument.recompute()
    vp.setEdit(fp)
    return fp

def makeDimple(base = None, green = False):
    '''Python command to create a Dimple.'''
    from Dimple import Dimple      
    reload(Dimple)     # causes FreeCAD to reload Dimple.py every time a new Dimple is created. Useful while developping the feature.      
    fp = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Dimple")
    Dimple.DimpleWorker(fp, base, green)
    vp = Dimple.DimpleViewProvider(fp.ViewObject)
    FreeCAD.ActiveDocument.recompute()
    vp.setEdit(fp)
    return fp
    
