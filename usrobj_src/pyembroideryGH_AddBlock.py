"""
Adds a block of stitches to an embroidery pattern supplied as
pyembroidery.EmbPattern instance
    Inputs:
        Pattern: The pattern to be modified as
                 pyembroidery.EmbPattern instance.
                 {item, EmbPattern}
        Stitches: The block(s) of stitches to add to the pattern. If a
                  tree is supplied, each branch will be treated as one block.
                  {list, str}
        Thread: The threads for the pattern, corresponding to
                the blocks of stitches. This is optional, If no thread is
                supplied, the blocks will still be added to the pattern!
                {item, EmbThread}
    Output:
        Pattern: The modified pattern with the blocks of stitches and the their
                 thread added.
                 {item/list/tree, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201104
"""

# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division
import re

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "AddBlock"
ghenv.Component.NickName = "AB"
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

class AddBlock(component):

    def RunScript(self, input_pattern, Stitches, Thread):
        # initialize output
        Pattern = Grasshopper.DataTree[object]()
        
        # check if valid data is coming in
        if input_pattern != None and Stitches:
            # check if pattern is valid
            if not isinstance(input_pattern, pyembroidery.EmbPattern):
                raise TypeError("The supplied pattern is not a valid " +
                                "pyembroidery.EmbPattern instance!")
            else:
                # copy input pattern to avoid changing the original
                Pattern = input_pattern.copy()
                # regex pattern for matching stitch strings
                regex = re.compile(r'^([+-]?(\d+([.]\d*)?([eE][+-]?\d+)?|[.]\d+([eE][+-]?\d+)?)[,]){2}[-+]?[0-9]+$')
                # check and extract stitches, compile valid_stitches
                valid_stitches = []
                for i, stitch in enumerate(Stitches):
                    if bool(regex.match(stitch)):
                        # convert the stitch
                        stitch = stitch.split(",")
                        stitch = (float(stitch[0]),
                                  float(stitch[1]),
                                  int(stitch[2]))
                        valid_stitches.append(stitch)
                    else:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("{}. stitch at index {} is not a " +
                                  "valid stitch string! Skipping this stitch!")
                        errMsg = errMsg.format(i, self.RunCount)
                        self.AddRuntimeMessage(rml, errMsg)
                if Thread != None:
                    if not isinstance(Thread, pyembroidery.EmbThread):
                        raise TypeError("The supplied thread is not a valid " +
                                        "pyembroidery.EmbThread instance!")
                else:
                    rml = self.RuntimeMessageLevel.Remark
                    errMsg = ("No Thread supplied. Resulting block will not " +
                              "have a thread attached.")
                    errMsg = errMsg.format(self.RunCount)
                    self.AddRuntimeMessage(rml, errMsg)
                # add the block and thread to the pattern
                Pattern.add_block(valid_stitches, Thread)
        else:
            rml = self.RuntimeMessageLevel.Warning
            if not Stitches:
                errMsg = ("Input Stitches failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
