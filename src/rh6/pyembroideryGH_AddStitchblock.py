"""Adds a stitchblock to an embroidery pattern supplied as
pyembroidery.EmbPattern instance
            Inputs:
                Pattern: The pattern to be modified as
                pyembroidery.EmbPattern instance. This works only on a single
                pattern for now!
                Stitch: The stitchblocks to add to the pattern. If a
                tree is supplied, each branch will be treated as one block.
                Thread: The threads for the pattern, corresponding to
                the blocks of stitches. The paths of the block and the thread
                have to correspond, otherwise the thread won't be found.
                If there's more than one thread in the branch, only the first
                thread will be used!
            Output:
                PatternOut: The modified pattern with the stitchblocks added
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

ghenv.Component.Name = "AddStitchblock"
ghenv.Component.NickName = "ASB"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pattern, Stitchblock):
        # initialize outputs
        PatternOut = Grasshopper.DataTree[object]()

        # copy the input pattern to avoid modification on the original object
        if isinstance(Pattern, pyembroidery.EmbPattern) == True:
            cPattern = Pattern.copy()
        else:
            raise TypeError("Supplied pattern is no valid " + \
                            "pyembroidery.EmbPattern instance! " + \
                            "Please check your inputs and try again.")

        # loop over all branches of the stitchblock tree
        for i in range(Stitchblock.BranchCount):
            branchList = Stitchblock.Branch(i)
            branchPath = Stitchblock.Path(i)

            # loop over all items in the current branch
            for j in range(branchList.Count):
                sBlock = branchList[j]

                # add stitchblock to the pattern
                cPattern.add_stitchblock(sBlock)

        # add pattern to output tree
        PatternOut.Add(cPattern)

        # return outputs if you have them; here I try it for you:
        return PatternOut
