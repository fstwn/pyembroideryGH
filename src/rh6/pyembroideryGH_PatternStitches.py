"""Get all the raw stitches of a pattern. The pattern has to be supplied
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
                License: Apache License 2.0
                Version: 191105"""

from __future__ import division
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import pyembroidery

ghenv.Component.Name = "PatternStitches"
ghenv.Component.NickName = "PSS"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

__author__ = "Max Eschenbach"
__version__ = "2019.11.05"

class MyComponent(component):

    def RunScript(self, Pattern):
        # initialize outputs
        X = None
        Y = None
        Cmd = None
        Thread = None
        Needle = None
        Order = None

        # only do something if there is an input to begin with
        if (Pattern != None and \
        isinstance(Pattern, Grasshopper.DataTree[object]) == True):
            # if the tree has more than one path it is a "real" tree
            if Pattern.BranchCount >= 1:
                # create GH Tree for all output params
                X = Grasshopper.DataTree[object]()
                Y = Grasshopper.DataTree[object]()
                Cmd = Grasshopper.DataTree[object]()
                Thread = Grasshopper.DataTree[object]()
                Needle = Grasshopper.DataTree[object]()
                Order = Grasshopper.DataTree[object]()
                # loop through all branches of the tree
                for i in range(Pattern.BranchCount):
                    branchList = Pattern.Branch(i)
                    branchPath = Pattern.Path(i)
                    # if there is more than one item in the branch
                    if branchList.Count > 1:
                        for j in range(branchList.Count):
                            # make sure supplied pattern is really valid
                            if not isinstance(branchList[j],
                                              pyembroidery.EmbPattern):
                                raise TypeError("The supplied pattern is " + \
                                                "not a valid pyembroidery." + \
                                                "EmbPattern instance!")
                            # Get the stitches of the pattern
                            stitches = zip(*list(
                                        branchList[j].get_as_stitches()))
                            # construct a new path for the outputs
                            path = list(branchPath)
                            path.append(j)
                            path = Grasshopper.Kernel.Data.GH_Path(*path)
                            # add the relevant data to the output trees
                            X.AddRange(list([s*0.1 for s in stitches[1]]), path)
                            Y.AddRange(list([s*0.1 for s in stitches[2]]), path)
                            Cmd.AddRange(list(stitches[3]), path)
                            Thread.AddRange(list(stitches[4]), path)
                            Needle.AddRange(list(stitches[5]), path)
                            Order.AddRange(list(stitches[6]), path)
                    # if there is only one item in the branch
                    elif branchList.Count == 1:
                        # make sure supplied pattern is really a valid pattern
                        if not isinstance(branchList[0],
                                          pyembroidery.EmbPattern):
                            raise TypeError("The supplied pattern is not a " + \
                                            "valid pyembroidery.EmbPattern " + \
                                            "instance!")
                        # Get the stitches of the pattern
                        stitches = zip(*list(
                                    branchList[0].get_as_stitches()))
                        # add the relevant data to the output trees
                        X.AddRange(list([s*0.1 for s in stitches[1]]),
                                        branchPath)
                        Y.AddRange(list([s*0.1 for s in stitches[2]]),
                                        branchPath)
                        Cmd.AddRange(list(stitches[3]), branchPath)
                        Thread.AddRange(list(stitches[4]), branchPath)
                        Needle.AddRange(list(stitches[5]), branchPath)
                        Order.AddRange(list(stitches[6]), branchPath)

        # return outputs if you have them; here I try it for you:
        return (X, Y, Cmd, Thread, Needle, Order)
