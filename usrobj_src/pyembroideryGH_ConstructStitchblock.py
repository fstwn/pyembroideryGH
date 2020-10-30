"""
Compile a StitchBlock from a list of stitches and a thread.
    Inputs:
        Stitches: The stitches to compile into a stitchblock.
                  {list, stitch}
        Thread: The thread to be attached to the stitchblock.
                {item, EmbThread}
    Output:
        StitchBlock: The newly compiled stitchblocks, containing the stitches
                     with the respective thread attached to it.
                     {item/list/tree, StitchBlock}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201030
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
ghenv.Component.Name = "ConstructStitchBlock"
ghenv.Component.NickName = "CSB"
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

class StitchBlock(object):
    
    def __init__(self, stitches, thread):
        self._set_stitches(stitches)
        self._set_thread(thread)
    
    def __getitem__(self, item):
        return (self.stitches, self.thread)[item]
    
    def get_stitches_iter(self):
        for s in self._stitches:
            yield s
    
    def _get_stitches(self):
        return self._stitches
    
    def _set_stitches(self, stitches):
        if isinstance(stitches, list):
            self._stitches = stitches
        elif isinstance(stitches, tuple):
            self._stitches = list(stitches)
        else:
            raise ValueError("Supplied data for stitches is not a valid list " +
                             "of stitches!")
    
    stitches = property(_get_stitches, _set_stitches, None,
                        "The stitches of this StitchBlock")
    
    def _get_thread(self):
        return self._thread
    
    def _set_thread(self, thread):
        if isinstance(thread, pyembroidery.EmbThread):
            self._thread = thread
        else:
            raise ValueError("Supplied thread is not a valid EmbThread " + 
                             "instance!")
    
    thread = property(_get_thread, _set_thread, None,
                      "The thread of this StitchBlock")
    
    def ToString(self):
        descr = "StitchBlock ({} Stitches, EmbThread {})"
        color = self.thread.hex_color()
        descr = descr.format(len(self.stitches), color)
        return descr

class ConstructStitchBlock(component):
    
    def RunScript(self, Stitches, Thread):
        
        if Stitches and Thread:
            # regex pattern for matching stitch strings
            regex = re.compile(r'^([+-]?(\d+([.]\d*)?([eE][+-]?\d+)?|[.]\d+([eE][+-]?\d+)?)[,]){2}[-+]?[0-9]+$')
            
            # check and extract stitches, compile valid_stitches
            valid_stitches = []
            for i, stitch in enumerate(Stitches):
                if bool(regex.match(stitch)):
                    # convert the stitch
                    stitch = stitch.split(",")
                    stitch = (float(stitch[0]), float(stitch[1]), int(stitch[2]))
                    valid_stitches.append(stitch)
                else:
                    rml = self.RuntimeMessageLevel.Warning
                    errMsg = ("{}. stitch at index {} is not a " +
                              "valid stitch string! Skipping this stitch!")
                    errMsg = errMsg.format(i, self.RunCount)
                    self.AddRuntimeMessage(rml, errMsg)
            
            # create stitchblock
            try:
                sblock = StitchBlock(valid_stitches, Thread)
            except Exception, e:
                rml = self.RuntimeMessageLevel.Warning
                errMsg = "Could not create StitchBlock at index {}!"
                errMsg = " ".join([errMsg, e]).format(self.RunCount)
                self.AddRuntimeMessage(rml, errMsg)
                sblock = None
        else:
            sblock = Grasshopper.DataTree[object]()
            rml = self.RuntimeMessageLevel.Warning
            if not Stitches:
                errMsg = ("Input Stitches failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
            if not Thread:
                errMsg = ("Input Thread failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return sblock
