"""
Adds one or many threads to the design (pattern)
Note: this has no effect on stitching and can be done at any point
    Inputs:
        Pattern: The pattern to be modified as
                 pyembroidery.EmbPattern instance.
                 {item, EmbPattern}
        Thread: The thread or multiple threads to add to the pattern as
                pyembroidery.EmbThread instanc.
                {list, EmbThread}
    Output:
        Pattern: The modified pattern with the thread or multiple threads
                 added.
                 {item/list/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201104
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
ghenv.Component.Name = "AddThread"
ghenv.Component.NickName = "AT"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class AddThread(component):

    def RunScript(self, input_pattern, Thread):
        # initialize outputs
        Pattern = Grasshopper.DataTree[object]()
        
        # check if valid data is coming in
        if input_pattern != None and Thread:
            # check if pattern is valid
            if not isinstance(input_pattern, pyembroidery.EmbPattern):
                raise TypeError("The supplied pattern is not a valid " +
                                "pyembroidery.EmbPattern instance!")
            
            # copy input pattern to avoid changing the original
            Pattern = input_pattern.copy()
            # loop over supplied list of threads
            for i, thrd in enumerate(Thread):
                if not isinstance(thrd, pyembroidery.EmbThread):
                    rml = self.RuntimeMessageLevel.Warning
                    errMsg = ("{}. thread at index {} is not a " +
                              "valid pyembroidery.EmbThread instance! " +
                              "Skipping this thread!")
                    errMsg = errMsg.format(i, self.RunCount)
                    self.AddRuntimeMessage(rml, errMsg)
                else:
                    # add thread to pattern
                    Pattern.add_thread(thrd)
        else:
            if input_pattern == None:
                rml = self.RuntimeMessageLevel.Warning
                errMsg = ("Input Pattern failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
            if not Thread:
                rml = self.RuntimeMessageLevel.Warning
                errMsg = ("Input Thread failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
