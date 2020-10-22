"""
Get all the raw stitches of a pattern. The pattern has to be supplied
as an instance of pyembroidery.EmbPattern.
    Inputs:
        Pattern: Pattern as pyembroidery EmbPattern instance
    Output:
        X: The X-Coordinate of the stitch
        Y: The Y-Coordinate of the stitch
        Cmd = The command for the stitch
        Thread: The thread of the stitch
        Needle: The needle of the stitch
        Order: The order of the stitch
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
ghenv.Component.Name = "PatternRawStitches"
ghenv.Component.NickName = "PRS"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class PatternRawStitches(component):

    def RunScript(self, Pattern):
        # initialize outputs
        X = Grasshopper.DataTree[object]()
        Y = Grasshopper.DataTree[object]()
        Cmd = Grasshopper.DataTree[object]()
        Thread = Grasshopper.DataTree[object]()
        Needle = Grasshopper.DataTree[object]()
        Order = Grasshopper.DataTree[object]()

        # only do something if there is an input to begin with
        if Pattern != None:
            # make sure supplied pattern is really a valid pattern
            if not isinstance(Pattern, pyembroidery.EmbPattern):
                rml = self.RuntimeMessageLevel.Error
                errMsg = ("The supplied pattern is not a valid" +
                          "pyembroidery.EmbPattern instance!")
                self.AddRuntimeMessage(rml, errMsg)
                return (X, Y, Cmd, Thread, Needle, Order)
            
            # Get the stitches of the pattern
            stitches = zip(*list(Pattern.get_as_stitches()))
            
            # collect the relevant data and assign it to the outputs
            X = tuple([s * 0.1 for s in stitches[1]])
            Y = tuple([s * -0.1 for s in stitches[2]])
            Cmd = stitches[3]
            Thread = stitches[4]
            Needle = stitches[5]
            Order = stitches[6]
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Expected EmbPattern, got None!")
            self.AddRuntimeMessage(rml, errMsg)

        # return outputs if you have them; here I try it for you:
        return (X, Y, Cmd, Thread, Needle, Order)
