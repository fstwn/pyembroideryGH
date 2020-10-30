"""
Adds one or many StitchBlocks to an embroidery pattern supplied as
pyembroidery.EmbPattern instance
    Inputs:
        Pattern: The pattern to be modified as pyembroidery.EmbPattern 
                 instance.
                 {item, EmbPattern}
        StitchBlock: The stitchblock(s) to add to the pattern.
                     {list, StitchBlock}
    Output:
        Pattern: The modified pattern with the newly added stitchblock(s).
                 {item/list/tree, EmbPattern}
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
ghenv.Component.Name = "AddStitchBlock"
ghenv.Component.NickName = "ASB"
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

class AddStitchBlock(component):

    def RunScript(self, pattern_in, stitchblock):
        # initialize outputs
        Pattern = Grasshopper.DataTree[object]()
        
        if pattern_in is not None and stitchblock:
            # copy the input pattern to avoid modification on the original object
            if isinstance(pattern_in, pyembroidery.EmbPattern):
                pattern_in = pattern_in.copy()
            else:
                raise TypeError("Supplied pattern is no valid " +
                                "pyembroidery.EmbPattern instance! " +
                                "Please check your inputs and try again.")
            
            # loop over all stitchblocks and add to pattern
            for i, sb in enumerate(stitchblock):
                pattern_in.add_stitchblock(sb)
            
            # add pattern to output tree
            Pattern.Add(pattern_in)
        else:
            rml = self.RuntimeMessageLevel.Warning
            if pattern_in is None:
                errMsg = ("Input Pattern failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
            if not stitchblock:
                errMsg = ("Input StitchBlock failed to collect data!")
                self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Pattern
