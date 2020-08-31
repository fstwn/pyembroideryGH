"""Deconstructs a stitch-string into its component parts
            Inputs:
                Stitch: The stitch to deconstruct, formatted as string
            Output:
                X: The X-Coordinate of the stitch
                Y: The Y-Coordinate of the stitch
                C: The command of the stitch as integer
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

ghenv.Component.Name = "DeconstructStitch"
ghenv.Component.NickName = "DS"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Stitch):
        # initialize outputs
        X = None
        Y = None
        Cmd = None

        # only do something if there is an incoming stitch-string to begin with
        if (Stitch != None and \
        isinstance(Stitch, Grasshopper.DataTree[object]) == True):
            # initialize all outputs as GH trees
            X = Grasshopper.DataTree[object]()
            Y = Grasshopper.DataTree[object]()
            Cmd = Grasshopper.DataTree[object]()

            # loop through all branches of the tree
            for i in range(Stitch.BranchCount):
                branchList = Stitch.Branch(i)
                branchPath = Stitch.Path(i)

                # loop through all items in the current branch
                for j in range(branchList.Count):
                    # split the string in its components
                    parts = branchList[j].split(",")

                    # add each component to its respective output tree
                    # !! WE MULTIPLY ALL COORDINATES WITH 0.1 BECAUSE ONE !!
                    # !! UNIT IN PYEMBROIDERY IS 1/10th OF A MILLIMETER   !!
                    X.Add(float(parts[0])*0.1, branchPath)
                    Y.Add(float(parts[1])*0.1, branchPath)
                    Cmd.Add(int(parts[2]), branchPath)

        # return outputs if you have them; here I try it for you:
        return (X, Y, Cmd)
