"""Get the stitches and threads of an embroidery pattern, formatted as
colorblocks. The pattern has to be supplied as an instance of
pyembroidery.EmbPattern.
            Inputs:
                Pattern: Pattern as pyembroidery.EmbPattern instance
            Output:
                Stitch: The stitch(es) formatted as colorblocks
                Thread: The thread, corresponding to the colorblock
                as pyembroidery.EmbThread instance.
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

ghenv.Component.Name = "PatternColorblocks"
ghenv.Component.NickName = "PCB"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

__author__ = "Max Eschenbach"
__version__ = "2019.11.05"

class MyComponent(component):

    def RunScript(self, Pattern):
        # initialize outputs
        Stitch = None
        Thread = None

        # only do something if there is a pattern to begin with
        if (Pattern != None and \
        isinstance(Pattern, Grasshopper.DataTree[object]) == True):
            # initialize the outputs as GH trees
            Stitch = Grasshopper.DataTree[object]()
            Thread = Grasshopper.DataTree[object]()

            # loop through all the branches of the incoming tree
            for i in range(Pattern.BranchCount):
                branchList = Pattern.Branch(i)
                branchPath = Pattern.Path(i)

                # loop through all items of the current branch
                for j in range(branchList.Count):
                    # make sure supplied pattern is really valid
                    if not isinstance(branchList[j], pyembroidery.EmbPattern):
                        raise TypeError("The supplied pattern is " + \
                                        "not a valid pyembroidery." + \
                                        "EmbPattern instance!")
                    # get the colorblocks of the pattern
                    stitchblock = zip(*list(branchList[j].get_as_colorblocks()))
                    blocks = list(stitchblock[0])
                    threads = list(stitchblock[1])

                    # loop through all blocks
                    for u in range(len(blocks)):
                        stitches = blocks[u]

                        # loop through all the stitches of the current block
                        for x in range(len(stitches)):
                            # convert the stitch data to strings
                            stitch = [str(s) for s in stitches[x]]
                            stitches[x] = stitch
                        # join the strings together to create the
                        # formatted stitch-string
                        stitches = [",".join(s) for s in stitches]

                        # create the new tree path by modding the original path
                        path = list(branchPath)
                        # if there is more than one pattern in the branch
                        if branchList.Count > 1:
                            path.append(j)
                            path.append(u)
                        else:
                            path.append(u)
                        path = Grasshopper.Kernel.Data.GH_Path(*path)

                        # add the stitch-strings to the output tree
                        Stitch.AddRange(stitches, path)

                    # loop through all corresponding threads of the colorblocks
                    for u in range(len(threads)):
                        # create the new tree path by modding the original path
                        path = list(branchPath)
                        # if there is more than one pattern in the branch
                        if branchList.Count > 1:
                            path.append(j)
                            path.append(u)
                        else:
                            path.append(u)
                        path = Grasshopper.Kernel.Data.GH_Path(*path)

                        # add the thread to the output tree
                        Thread.Add(threads[u], path)

        # return outputs if you have them; here I try it for you:
        return (Stitch, Thread)
