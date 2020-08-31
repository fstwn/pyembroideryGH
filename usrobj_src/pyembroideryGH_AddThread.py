"""Adds one or many threads to the design (pattern)
Note: this has no effect on stitching and can be done at any point
            Inputs:
                Pattern: The pattern to be modified as
                pyembroidery.EmbPattern instance. This works only on a single
                pattern for now!
                Thread: The thread or threads to add to the pattern
            Output:
                PatternOut: The modified pattern with the threads added
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

ghenv.Component.Name = "AddThread"
ghenv.Component.NickName = "AT"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pattern, Thread):
        # initialize outputs
        PatternOut = Grasshopper.DataTree[object]()
        cPattern = None

        # copy the input pattern to avoid modification on the original object
        if isinstance(Pattern, pyembroidery.EmbPattern) == True:
            cPattern = Pattern.copy()
        else:
            raise TypeError("Supplied pattern is no valid " + \
                            "pyembroidery.EmbPattern instance! " + \
                            "Please check your inputs and try again.")

        # loop over all branches of the thread tree
        for i in range(Thread.BranchCount):
            branchList = Thread.Branch(i)
            branchPath = Thread.Path(i)

            # loop over all items in the current branch of threads
            for j in range(branchList.Count):
                thrd = branchList[j]
                print thrd
                # ensure that threads are real threads
                if isinstance(thrd, pyembroidery.EmbThread) != True:
                    raise TypeError("Supplied threads are no valid " + \
                                    "pyembroidery.EmbThread instances! " + \
                                    "Please check your inputs and try " + \
                                    "again.")
                # add threads to pattern
                cPattern.add_thread(thrd)

        # define outputs
        PatternOut = cPattern

        # return outputs if you have them; here I try it for you:
        return PatternOut
