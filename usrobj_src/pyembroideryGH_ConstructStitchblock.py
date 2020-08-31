"""Provides a scripting component.
            Inputs:
                Stitch: The x script variable
                Thread: The y script variable
            Output:
                Stitchblock: The a output variable
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

ghenv.Component.Name = "ConstructStitchblock"
ghenv.Component.NickName = "CSB"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Stitch, Thread):
        # initialize output
        Stitchblock = Grasshopper.DataTree[object]()

        # loop over all branches of the stitch tree
        for i in range(Stitch.BranchCount):
            branchList = Stitch.Branch(i)
            branchPath = Stitch.Path(i)

            # find the corresponding thread
            if Thread.PathExists(branchPath):
                try:
                    tList = list(Thread.Branch(branchPath))
                    thread = tList[0]
                    # ensure that threads are real threads
                    if isinstance(thread, \
                    pyembroidery.EmbThread) != True:
                        raise TypeError("Supplied threads are no valid " + \
                                        "pyembroidery.EmbThread instances! " + \
                                        "Please check your inputs and try " + \
                                        "again.")
                except IndexError:
                    thread = None
            else:
                thread = None

            # convert stitches to a block
            block = []
            for j in range(branchList.Count):
                # convert the stitch
                stitch = branchList[j].split(",")
                stitch = (float(stitch[0]), float(stitch[1]), int(stitch[2]))
                block.append(stitch)

            sBlock = [block, thread]

            # add stitchblocks to output
            Stitchblock.Add(sBlock, branchPath)

        # return outputs if you have them; here I try it for you:
        return Stitchblock
