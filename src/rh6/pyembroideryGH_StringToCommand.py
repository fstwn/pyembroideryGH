"""Converts any embroidery command from its String-form into
its Integer representation.
            Inputs:
                CmdStr: The embroidery command as String
            Output:
                Cmd: The converted embroidery command as Integer
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

ghenv.Component.Name = "StringToCommand"
ghenv.Component.NickName = "STC"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "0 Commands"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class StrToCmd(component):

    def RunScript(self, CmdStr):
        # initialize output
        Cmd = None
        # retrieve command dictionary for translation
        command_dict = pyembroidery.get_command_dictionary()
        # only do sth if there is valid input to begin with
        if (CmdStr != None and \
        isinstance(CmdStr, Grasshopper.DataTree[object]) == True):
            # initialize output as GH tree
            Cmd = Grasshopper.DataTree[object]()
            # loop through all branches of the tree
            for i in range(CmdStr.BranchCount):
                branchList = CmdStr.Branch(i)
                branchPath = CmdStr.Path(i)
                # loop through all items in the current branch
                for j in range(branchList.Count):
                    # look up the command in the dict and add the result to
                    # the output tree
                    Cmd.Add(command_dict.get(branchList[j]), branchPath)

        # return outputs if you have them; here I try it for you:
        return Cmd
