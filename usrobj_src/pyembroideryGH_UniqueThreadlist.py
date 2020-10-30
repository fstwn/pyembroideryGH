"""
Gets the threads of one or many input patterns as a unique list.
    Inputs:
        Pattern: The pattern to be modified as pyembroidery.EmbPattern 
                 instance.
                 {item, EmbPattern}
    Output:
        Thread: The threads of the pattern as
                pyembroidery.EmbThread instance.
                {item/list/tree, EmbThread}
    Remarks:
        Author: Max Eschenbach
        License: Apache License 2.0
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

ghenv.Component.Name = "UniqueThreadList"
ghenv.Component.NickName = "UTL"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class UniqueThreadList(component):

    def RunScript(self, Pattern):
        # initialize output tree
        Thread = Grasshopper.DataTree[object]()
        
        # make sure supplied pattern is really a valid pattern
        if Pattern is not None:
            if not isinstance(Pattern, pyembroidery.EmbPattern):
                raise TypeError("The supplied pattern is not a valid " +
                                "pyembroidery.EmbPattern instance!")
            else:
                # get the threadlist of the pattern
                Thread = Pattern.threadlist
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Input Pattern failed to collect data!")
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Thread
