"""Constructs a Stitch-String in the format "PtX,PtY,Cmd"
            Inputs:
                Pt: The input Point(s)
                Cmd: The corresponding Command for each point coordinate
            Output:
                Stitch: The data for the stitch as String
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

ghenv.Component.Name = "ConstructStitch"
ghenv.Component.NickName = "CS"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pt, Cmd):
        # initialize ouputs
        Stitch = None

        # only do something if there is data to begin with
        if (Pt != None and Cmd != None and \
        isinstance(Pt, Grasshopper.DataTree[object]) == True and \
        isinstance(Cmd, Grasshopper.DataTree[object]) == True):
            # case: both inputs as trees with more than one path
            if Pt.BranchCount > 1 and Cmd.BranchCount > 1:
                # subcase: both BranchCount and number of items are identical
                pt_ipb = [len(br) for br in Pt.Branches]
                cmd_ipb = [len(br) for br in Cmd.Branches]
                if pt_ipb == cmd_ipb:
                    Stitch = Grasshopper.DataTree[object]()
                    for i in range(Pt.BranchCount):
                        branchList = Pt.Branch(i)
                        branchPath = Pt.Path(i)
                        for j in range(branchList.Count):
                            pt = list(branchList[j])
                            comm = Cmd.Branch(i)[j]
                            stitch_str = (",".join([str(pt[0]*10),
                                            str(pt[1]*10), str(comm)]))
                            Stitch.Add(stitch_str, branchPath)
                # subcase: branchcount and number of items are not identical
                elif pt_ipb != cmd_ipb:
                    # sub-subcase: only branchcount is identical
                    if (Pt.BranchCount == Cmd.BranchCount and \
                    cmd_ipb == [1 for b in Cmd.Branches]):
                        Stitch = Grasshopper.DataTree[object]()
                        for i in range(Pt.BranchCount):
                            branchList = Pt.Branch(i)
                            branchPath = Pt.Path(i)
                            for j in range(branchList.Count):
                                pt = list(branchList[j])
                                comm = Cmd.Branch(i)[0]
                                stitch_str = (",".join([str(pt[0]*10),
                                                str(pt[1]*10), str(comm)]))
                                Stitch.Add(stitch_str, branchPath)
                    # both branchcount and items per branch differ completely
                    else:
                        raise NotImplementedError("Combining a tree of " + \
                            "points with a tree of commands that is " + \
                            "fundamentally different in structure " + \
                            "is not implemented yet! Still thinking of a " + \
                            "useful way to handle this...")
            # case: tree of points and flat list or single item
            elif Pt.BranchCount > 1 and Cmd.BranchCount == 1:
                # subcase: cmd is a flat list
                # behaviour: thinking of something useful...
                if Cmd.Branch(0).Count > 1:
                    raise NotImplementedError("The combination of a tree " + \
                            "of points and flat list of commands has not " + \
                            "been implemented yet! Still thinking of a " + \
                            "useful way to handle this...")
                # subcase: cmd is one single item
                # behaviour: cmd is applied to the whole tree of stitch-points
                elif Cmd.Branch(0).Count == 1:
                    Stitch = Grasshopper.DataTree[object]()
                    for i in range(Pt.BranchCount):
                        branchList = Pt.Branch(i)
                        branchPath = Pt.Path(i)
                        for j in range(branchList.Count):
                            pt = list(branchList[j])
                            comm = Cmd.Branch(0)[0]
                            stitch_str = (",".join([str(pt[0]*10),
                                              str(pt[1]*10), str(comm)]))
                            Stitch.Add(stitch_str, branchPath)
            # case: both inputs are flat
            elif Pt.BranchCount == 1 and Cmd.BranchCount == 1:
                # subcase: both BranchCount and number of items are identical
                pt_ipb = [len(br) for br in Pt.Branches]
                cmd_ipb = [len(br) for br in Cmd.Branches]
                if pt_ipb == cmd_ipb:
                    Stitch = Grasshopper.DataTree[object]()
                    for i in range(Pt.BranchCount):
                        branchList = Pt.Branch(i)
                        branchPath = Pt.Path(i)
                        for j in range(branchList.Count):
                            pt = list(branchList[j])
                            comm = Cmd.Branch(i)[j]
                            stitch_str = (",".join([str(pt[0]*10),
                                            str(pt[1]*10), str(comm)]))
                            Stitch.Add(stitch_str, branchPath)
                elif pt_ipb != cmd_ipb and cmd_ipb == [1]:
                    Stitch = Grasshopper.DataTree[object]()
                    for i in range(Pt.BranchCount):
                        branchList = Pt.Branch(i)
                        branchPath = Pt.Path(i)
                        for j in range(branchList.Count):
                            pt = list(branchList[j])
                            comm = Cmd.Branch(0)[0]
                            stitch_str = (",".join([str(pt[0]*10),
                                              str(pt[1]*10), str(comm)]))
                            Stitch.Add(stitch_str, branchPath)
        # return outputs if you have them; here I try it for you:
        return Stitch
