"""
Deconstructs a stitch-string into its component parts, which are x and y
coordinates as well as an integer identifying the command.
    Inputs:
        Stitch: The stitch to deconstruct, formatted as string
                {tree, str}
    Output:
        X: The X-Coordinate of the stitch as float.
           {item/list/tree, float}
        Y: The Y-Coordinate of the stitch as float.
           {item/list/tree, float}
        C: The command of the stitch as integer.
           {item/list/tree, int}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201022
"""

# GHPYTHON SDK IMPORTS
from __future__ import division
import re

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS 
ghenv.Component.Name = "DeconstructStitch"
ghenv.Component.NickName = "DS"
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

class DeconstructStitch(component):

    def RunScript(self, StitchTree):
        # initialize outputs
        X = Grasshopper.DataTree[object]()
        Y = Grasshopper.DataTree[object]()
        Cmd = Grasshopper.DataTree[object]()
        
        # regex pattern for matching stitch strings
        regex = re.compile(r'^([+-]?(\d+([.]\d*)?([eE][+-]?\d+)?|[.]\d+([eE][+-]?\d+)?)[,]){2}[-+]?[0-9]+$')
        
        # only do something if there is an incoming stitch-string to begin with
        if StitchTree != None:
            # loop through all branches of the tree
            for i, branch in enumerate(StitchTree.Branches):
                branch_path = StitchTree.Path(i)
                
                # loop through all items in the current branch
                for j, stitch_string in enumerate(branch):
                    if bool(regex.match(stitch_string)):
                        # split the string in its components
                        parts = stitch_string.split(',')
                        # add each component to its respective output tree
                        X.Add(float(parts[0]), branch_path)
                        Y.Add(float(parts[1]), branch_path)
                        Cmd.Add(int(parts[2]), branch_path)
                    else:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("Item at branch {}, index {} is not a " +
                                  "valid stitch string! A Null item will " +
                                  "be inserted into the output tree!")
                        errMsg = errMsg.format(i, j)
                        self.AddRuntimeMessage(rml, errMsg)
                        X.Add(None, branch_path)
                        Y.Add(None, branch_path)
                        Cmd.Add(None, branch_path)
                        continue
        
        # return outputs if you have them; here I try it for you:
        return X, Y, Cmd

