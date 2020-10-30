"""
Converts any valid embroidery command from integer into
its string representation.
    Inputs:
        Cmd: The embroidery command as integer.
             {tree, int}
    Output:
        CmdStr: The converted embroidery command as string if the input integer
                is valid, otherwise Null.
                {tree, str}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201030
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
ghenv.Component.Name = "CommandToString"
ghenv.Component.NickName = "CTS"
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

class CommandToString(component):
    
    def RunScript(self, CmdTree):
        # initialize output
        CmdStr = Grasshopper.DataTree[object]()
        
        # retrieve common dictionary to translate commands
        common_dict = pyembroidery.get_common_name_dictionary()
        
        # only do something if there is valid input to begin with
        if CmdTree != None and CmdTree.DataCount:
            # loop through all branches of the tree
            for i, branch in enumerate(CmdTree.Branches):
                branch_path = CmdTree.Path(i)
                # loop through all items in the current branch
                for j, command in enumerate(branch):
                    # look up the command in the dict and add the result to
                    # the output tree
                    try:
                        CmdStr.Add(common_dict[command], branch_path)
                    except KeyError:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("Command '{}' at branch {}, index {} " +
                                  "is not a known embroidery command integer!" +
                                  " A Null item will be inserted into the " +
                                  "output tree!")
                        errMsg = errMsg.format(command, i, j)
                        self.AddRuntimeMessage(rml, errMsg)
                        CmdStr.Add(None, branch_path)
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = "Input Cmd failed to collect data!"
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return CmdStr
