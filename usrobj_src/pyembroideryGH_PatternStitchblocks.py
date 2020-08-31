"""
Get the stitches and threads of an embroidery pattern, formatted as
stitchblocks. The pattern has to be supplied as an instance of
pyembroidery.EmbPattern.
    Inputs:
        Pattern: Pattern as pyembroidery.EmbPattern instance
    Output:
        Stitch: The stitch(es) of the stitchblocks
        Thread: The thread corresponding to the stitchblocks as
        pyembroidery.EmbThread instance
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
ghenv.Component.Name = "PatternStitchblocks"
ghenv.Component.NickName = "PSB"
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

class PatternStitchblocks(component):
    
    def RunScript(self, PatternTree):
        # initialize outputs
        Stitch = Grasshopper.DataTree[object]()
        Thread = Grasshopper.DataTree[object]()
        
        # only do something if there is an input to begin with.
        if PatternTree != None:
            # loop through all branches of the incoming tree(s)
            for i, branch in enumerate(PatternTree.Branches):
                branch_path = PatternTree.Path(i)
                
                # loop through all items of the current branch
                for j, pattern in enumerate(branch):
                    
                    # make sure supplied pattern is really valid
                    if not isinstance(pattern, pyembroidery.EmbPattern):
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("The supplied pattern at branch {}, " +
                                  "index {} is not a valid pyembroidery." + 
                                  "EmbPattern instance! Null items will be " + 
                                  "inserted into the output trees!")
                        errMsg = errMsg.format(i, j)
                        self.AddRuntimeMessage(rml, errMsg)
                        # create the new tree path by modding the original path
                        path = list(branch_path)
                        path.append(j)
                        path.append(0)
                        path = Grasshopper.Kernel.Data.GH_Path(*path)
                        Stitch.Add(None, path)
                        Thread.Add(None, path)
                        continue
                    
                    # get the stitchblocks of the pattern
                    stitchblock = zip(*list(pattern.get_as_stitchblock()))
                    blocks = stitchblock[0]
                    threads = stitchblock[1]
                    
                    # loop through all of the blocks of stitches
                    for u, block in enumerate(blocks):
                        stitches = list(block)
                        stitches = [",".join([str(s) for s in st])
                                    for st in stitches]
                        
                        # create the new tree path by modding the original path
                        path = list(branch_path)
                        path.append(j)
                        path.append(u)
                        path = Grasshopper.Kernel.Data.GH_Path(*path)
                        
                        # add all the stitches to the output tree
                        Stitch.AddRange(stitches, path)
                    
                    # loop through all of the threads
                    for u, thread in enumerate(threads):
                        # create the new tree path by modding the original path
                        path = list(branch_path)
                        path.append(j)
                        path.append(u)
                        path = Grasshopper.Kernel.Data.GH_Path(*path)
                        
                        # add all the threads to the output tree
                        Thread.Add(thread, path)
        
        # return outputs if you have them; here I try it for you:
        return Stitch, Thread
