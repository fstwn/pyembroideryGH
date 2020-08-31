"""Gets the threads of one or many input patterns
            Inputs:
                Pattern: The embroidery pattern
                as pyembroidery.EmbPattern instance
            Output:
                Thread: The threads of the pattern as
                        pyembroidery.EmbThread instance
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

ghenv.Component.Name = "Threadlist"
ghenv.Component.NickName = "TL"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pattern):
        # initialize output tree
        Thread = Grasshopper.DataTree[object]()

        # loop through all the branches in the pattern-tree
        for i in range(Pattern.BranchCount):
            branchList = Pattern.Branch(i)
            branchPath = Pattern.Path(i)

            # loop through all the items in the current branch
            # of the pattern tree
            for j in range(branchList.Count):
                # if there is only one pattern in the branch
                if branchList.Count == 1:
                    ptrn = branchList[j]
                    # check if pattern is really a valid embroidery pattern
                    if isinstance(ptrn, pyembroidery.EmbPattern) == True:
                        # get the threadlist of the pattern
                        threadList = ptrn.threadlist
                        # add all the threads to the output tree
                        for t in threadList:
                            Thread.Add(t, branchPath)
                    else:
                        raise TypeError("The supplied pattern is " + \
                                        "not a valid pyembroidery." + \
                                        "EmbPattern instance!")
                # if there is more than one pattern in the branch
                elif branchList.Count > 1:
                    ptrn = branchList[j]
                    # check if pattern is really a valid embroidery pattern
                    if isinstance(ptrn, pyembroidery.EmbPattern) == True:
                        # get the threadlist of the pattern
                        threadList = ptrn.threadlist
                        # modify the path for output
                        newPath = list(branchPath)
                        newPath.append(j)
                        newPath = Grasshopper.Kernel.Data.GH_Path(*newPath)
                        # add all the threads to the output tree
                        for t in threadList:
                            Thread.Add(t, newPath)
                    else:
                        raise TypeError("The supplied pattern is " + \
                                        "not a valid pyembroidery." + \
                                        "EmbPattern instance!")
        # return outputs if you have them; here I try it for you:
        return Thread
