"""Converts any embroidery command from its integer-form into
its string representation.
            Inputs:
                Cmd: The embroidery command as Integer
            Output:
                CmdStr: The converted embroidery command as string
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

ghenv.Component.Name = "CommandToString"
ghenv.Component.NickName = "CTS"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "0 Commands"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Cmd):
        # initialize output
        CmdStr = None
        # retrieve common dictionary to translate commands
        common_dict = pyembroidery.get_common_name_dictionary()

        # only do something if there is valid input to begin with
        if (Cmd != None and \
        isinstance(Cmd, Grasshopper.DataTree[object]) == True):
            # initialize output as GH tree
            CmdStr = Grasshopper.DataTree[object]()
            # loop through all branches of the tree
            for i in range(Cmd.BranchCount):
                branchList = Cmd.Branch(i)
                branchPath = Cmd.Path(i)
                # loop through all items in the current branch
                for j in range(branchList.Count):
                    # look up the command in the dict and add the result to
                    # the output tree
                    CmdStr.Add(common_dict.get(branchList[j]), branchPath)

        # return outputs if you have them; here I try it for you:
        return CmdStr
