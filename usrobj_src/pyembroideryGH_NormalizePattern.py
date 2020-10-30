"""
Encodes a pattern supplied as a pyembroidery.EmbPattern instance typically
for saving
    Inputs:
        Pattern: The embroidery pattern to normalize as
                 pyembroidery.EmbPattern instance
                 {item, EmbPattern}
    Output:
        Pattern: The normalized embroidery pattern as 
                 pyembroidery.EmbPattern instance
                 {item/ist/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: Apache License 2.0
        Version: 201030
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
ghenv.Component.Name = "NormalizePattern"
ghenv.Component.NickName = "NP"
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

class NormalizePattern(component):

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
                Pattern = input_pattern.get_normalized_pattern()
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Input Pattern failed to collect data!")
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
