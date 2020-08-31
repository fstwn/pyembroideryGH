"""
Reads any readable embroidery format and returns the
pattern as an instance of pyembroidery.EmbPattern
    Inputs:
        FilePath: Filepath of the embroidery pattern file.
                  {item, path}
    Output:
        Pattern: The embroidery pattern as pyembroidery.EmbPattern instance.
                 {item/list/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 200831
"""

# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division
from os import path

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "PatternRead"
ghenv.Component.NickName = "PR"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "1 Input/Output"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class PatternRead(component):

    def RunScript(self, FilePath):
        # Initialize output
        Pattern = Grasshopper.DataTree[object]()
        
        # only do something if input is defined
        if FilePath != None:
            try:
                Pattern = pyembroidery.read(path.normpath(
                                                    FilePath.strip("\n\r")))
            except Exception as e:
                rml = self.RuntimeMessageLevel.Error
                errMsg = ("Could not read embroidery file!" +
                          "Please check if format is readable.")
                self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
