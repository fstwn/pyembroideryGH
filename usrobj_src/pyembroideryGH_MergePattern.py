"""
Merges several embroidery patterns into a single pattern.
It accounts for some edge conditions but not all of them.

If there is an end command on the current pattern, that is removed.
If the color ending the current pattern is equal to the color starting the
next those color blocks are merged.
Any prepended thread change command to the merging pattern is suppressed.
    Inputs:
        Pattern: The list of patterns to be merged into one pattern.
                 {list, EmbPattern}
    Output:
        Pattern: The merged pattern.
                 {item/list/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201030
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
ghenv.Component.Name = "MergePattern"
ghenv.Component.NickName = "MP"
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

class MergePattern(component):

    def RunScript(self, Patterns):
        # initialize outputs
        MergedPattern = Grasshopper.DataTree[object]()
        
        if Patterns:
            for i, pat in enumerate(Patterns):
                # check input data correctness
                if isinstance(pat, pyembroidery.EmbPattern):
                    # copy first pattern to the merged pattern
                    if i == 0:
                        MergedPattern = pat.copy()
                    else:
                        MergedPattern = MergedPattern + pat
                else:
                    rml = self.RuntimeMessageLevel.Warning
                    errMsg = ("Supplied pattern at branch {0}, index {1} is no "
                              "valid instance of pyembroidery.EmbPattern! It was "
                              "skipped during the merge!")
                    errMsg = errMsg.format(self.RunCount, i)
                    self.AddRuntimeMessage(rml, errMsg)
                    continue
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Input Pattern failed to collect data!")
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return MergedPattern
