"""Create one or a collection of empty embroidery patterns as
instances of pyembroidery.EmbPattern
            Inputs:
                N: The number of empty patterns to be created, 1 if left blank
            Output:
                PatternOut: The empty pyembroidery.EmbPattern instance
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

ghenv.Component.Name = "CreatePattern"
ghenv.Component.NickName = "CP"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, N):
        # default for N
        if not N or N == None or N.DataCount == 0:
            N.Add(1)

        # initialize output
        PatternOut = Grasshopper.DataTree[object]()

        # loop through all branches of the tree
        for i in range(N.BranchCount):
            branchList = N.Branch(i)
            branchPath = N.Path(i)

            # loop through all items in the current branch
            for j in range(branchList.Count):
                num_pats = branchList[j]
                # create empty patterns
                for x in range(num_pats):
                    pat = pyembroidery.EmbPattern()
                    PatternOut.Add(pat, branchPath)

        # return outputs if you have them; here I try it for you:
        return PatternOut
