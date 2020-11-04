"""
Gets a stablized version of the pattern
    Inputs:
        Pattern: The embroidery pattern to stabilize.
                 {item, EmbPattern}
    Output:
        Pattern: The stabilized embroidery pattern
                 {item/list/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201104
"""

# PYTHON STANDARD LIBRARY INPUTS
from __future__ import division

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "StabilizePattern"
ghenv.Component.NickName = "SP"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "4 Utility"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class StabilizePattern(component):

    def RunScript(self, input_pattern):
        # initialize output as empty GH tree
        Pattern = Grasshopper.DataTree[object]()
        
        # make sure supplied pattern is really a valid pattern
        if input_pattern:
            if not isinstance(input_pattern, pyembroidery.EmbPattern):
                raise TypeError("The supplied pattern is not a valid " +
                                "pyembroidery.EmbPattern instance!")
            else:
                # don't modify the incoming pattern, make a copy and modify
                Pattern = input_pattern.get_stable_pattern()
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Input Pattern failed to collect data!")
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
