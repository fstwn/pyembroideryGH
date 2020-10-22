"""
Create one or a collection of empty embroidery patterns as
instances of pyembroidery.EmbPattern.
    Inputs:
        N: The number of empty patterns to be created, 1 if left blank.
           {item, int}
    Output:
        Pattern: The empty pattern as a pyembroidery.EmbPattern instance.
                 {item/list/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201022
"""

# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "CreatePattern"
ghenv.Component.NickName = "CP"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class CreatePattern(component):

    def RunScript(self, N):
        # default for N
        if N is None:
            N = 1
        
        # initialize output
        Pattern = System.Collections.Generic.List[object]()
        
        # create empty patterns
        for i in range(N):
            pat = pyembroidery.EmbPattern()
            Pattern.Add(pat)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
