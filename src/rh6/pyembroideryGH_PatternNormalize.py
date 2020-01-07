"""Encodes a pattern supplied as a pyembroidery.EmbPattern instance typically
for saving
            Inputs:
                Pattern: The embroidery pattern to normalize
                as pyembroidery.EmbPattern instance
            Output:
                PatternOut: The normalized embroidery pattern
                as pyembroidery.EmbPattern instance
            Remarks:
                Author: Max Eschenbach
                License: Apache License 2.0
                Version: 191104"""

from __future__ import division
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import pyembroidery

ghenv.Component.Name = "PatternNormalize"
ghenv.Component.NickName = "PN"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "4 Utility"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pattern):
        # initialize output as empty GH tree
        PatternOut = Grasshopper.DataTree[object]()

        # loop through all branches of the incoming tree
        for i in range(Pattern.BranchCount):
            branchList = Pattern.Branch(i)
            branchPath = Pattern.Path(i)
            # loop through all items in current branch
            for j in range(branchList.Count):
                # make sure supplied pattern is really a valid pattern
                if not isinstance(branchList[j], pyembroidery.EmbPattern):
                    raise TypeError("The supplied pattern is not a valid " + \
                                    "pyembroidery.EmbPattern instance!")
                # don't modify the incoming pattern, make a copy and modify that
                cPattern = branchList[j].get_normalized_pattern()
                # add modified pattern to output tree
                PatternOut.Add(cPattern, branchPath)

        # return outputs if you have them; here I try it for you:
        return PatternOut
