"""
Constructs a Stitch-String in the format (PtX, PtY, Cmd) by pairing each input
coordinate with an input command.
    Inputs:
        Pt: The input coordinate (point) for the stitch.
            {list, point3d}
        Cmd: The corresponding command integer for each point coordinate.
             {list, int}
    Output:
        Stitch: The constructed stitch as String.
                {item/list/tree, str}
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
ghenv.Component.Name = "ConstructStitch"
ghenv.Component.NickName = "CS"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

class ConstructStitch(component):

    def RunScript(self, Pt, Cmd):
        # initialize ouputs
        Stitches = []
        
        # only act if there is some data to begin with
        if Pt and Cmd:
            # list of points is longer or equal to list of commands, so we
            # loop over the list of points
            if len(Pt) >= len(Cmd):
                for i, pt in enumerate(Pt):
                    # extract command with failsafe
                    if i <= len(Cmd) - 1:
                        command = Cmd[i]
                    else:
                        command = Cmd[-1]
                    # compile stitch string
                    stitch_str = ",".join([str(pt.X * 10), 
                                           str(pt.Y * -10),
                                           str(command)])
                    # append to list of stitches
                    Stitches.append(stitch_str)
            # list of commands is longer than list of points, so we have to
            # loop over the list of commands
            elif len(Pt) < len(Cmd):
                for j, command in enumerate(Cmd):
                    # extract coordinate with failsafe
                    if j <= len(Pt) - 1:
                        pt = Pt[j]
                    else:
                        pt = Pt[-1]
                    # compile stitch string
                    stitch_str = ",".join([str(pt.X * 10),
                                           str(pt.Y * -10),
                                           str(command)])
                    # append to list of stitches
                    Stitches.append(stitch_str)
        else:
            rml = self.RuntimeMessageLevel.Warning
            if not Pt:
                errMsg = "Input Pt failed to collect data!"
                self.AddRuntimeMessage(rml, errMsg)
            if not Cmd:
                errMsg = "Input Cmd failed to collect data!"
                self.AddRuntimeMessage(rml, errMsg)
            return Grasshopper.DataTree[object]()
        
        # return outputs if you have them; here I try it for you:
        return Stitches
