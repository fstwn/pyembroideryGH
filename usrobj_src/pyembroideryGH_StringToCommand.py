"""
Converts any valid embroidery command from string into
its integer representation.
    Inputs:
        CmdStr: The embroidery command as string.
                {tree, str}
    Output:
        Cmd: The converted embroidery command as integer if the input string
             is valid, otherwise Null.
             {tree, int}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 200831
"""

# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS 
ghenv.Component.Name = "StringToCommand"
ghenv.Component.NickName = "STC"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "0 Commands"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class StringToCommand(component):

    def RunScript(self, CmdStrTree):
        # initialize output as GH tree
        Cmd = Grasshopper.DataTree[object]()
        
        # retrieve command dictionary for translation
        command_dict = pyembroidery.get_command_dictionary()
        
        # only do sth if there is valid input to begin with
        if CmdStrTree != None:
            # loop through all branches of the tree
            for i, branch in enumerate(CmdStrTree.Branches):
                branch_path = CmdStrTree.Path(i)
                # loop through all items in the current branch
                for j, command in enumerate(branch):
                    # look up the command in the dict and add the result to
                    # the output tree
                    try:
                        Cmd.Add(command_dict[command], branch_path)
                    except KeyError:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("Command '{}' at branch {}, index {} " +
                                  "is not a known embroidery command string!" +
                                  " A Null item will be inserted into the " +
                                  "output tree!")
                        errMsg = errMsg.format(command, i, j)
                        self.AddRuntimeMessage(rml, errMsg)
                        Cmd.Add(None, branch_path)
        
        # return outputs if you have them; here I try it for you:
        return Cmd
