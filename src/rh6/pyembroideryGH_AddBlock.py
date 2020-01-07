"""Adds a block of stitches to an embroidery pattern supplied as
pyembroidery.EmbPattern instance
            Inputs:
                Pattern: The pattern to be modified as
                pyembroidery.EmbPattern instance. This works only on a single
                pattern for now!
                Stitch: The block(s) of stitches to add to the pattern. If a
                tree is supplied, each branch will be treated as one block.
                Thread: The threads for the pattern, corresponding to
                the blocks of stitches. The paths of the block and the thread
                have to correspond, otherwise the thread won't be found.
                If there's more than one thread in the branch, only the first
                thread will be used!
            Output:
                PatternOut: The modified pattern with the stitches added
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

ghenv.Component.Name = "AddBlock"
ghenv.Component.NickName = "AB"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pattern, Stitch, Thread):
        # initialize outputs
        PatternOut = Grasshopper.DataTree[object]()

        # copy the input pattern to avoid modification on the original object
        if isinstance(Pattern, pyembroidery.EmbPattern) == True:
            cPattern = Pattern.copy()
        else:
            raise TypeError("Supplied pattern is no valid " + \
                            "pyembroidery.EmbPattern instance! " + \
                            "Please check your inputs and try again.")

        stitches = []
        blocks = []
        # loop over all branches of the stitch tree
        for i in range(Stitch.BranchCount):
            branchList = Stitch.Branch(i)
            branchPath = Stitch.Path(i)
            # define list for block
            block = []
            ptBlock = []
            # loop over all items in the current branch of stitches
            for j in range(branchList.Count):
                # convert the stitch
                stitch = branchList[j].split(",")
                stitch = [float(stitch[0]), float(stitch[1]), int(stitch[2])]
                block.append(stitch)

                # append to list for preview
                ptSt = [stitch[0]*0.1, stitch[1]*0.1, stitch[2]]
                stitches.append(ptSt)
                ptBlock.append(ptSt)
            blocks.append(ptBlock)
            # check for corresponding threads for the block of stitches
            if Thread.PathExists(branchPath):
                try:
                    # get the list of items in the branchpath
                    tList = list(Thread.Branch(branchPath))
                    thread = tList[0]
                    # ensure that threads are real threads
                    if isinstance(thread, \
                    pyembroidery.EmbThread.EmbThread) != True:
                        raise TypeError("Supplied threads are no valid " + \
                                        "pyembroidery.EmbThread instances! " + \
                                        "Please check your inputs and try " + \
                                        "again.")
                except IndexError:
                    thread = None
            else:
                thread = None

            # add the block with corresponding thread to the pattern
            cPattern.add_block(block, thread)

        # define outputs
        PatternOut.Add(cPattern)

        # add to document for preview
        #stitches = [rs.AddPoint(pt) for pt in stitches]
        #polys = [rs.AddPolyline(polypts) for polypts in blocks]

        # return outputs if you have them; here I try it for you:
        return PatternOut
