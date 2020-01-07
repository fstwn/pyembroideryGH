"""Reads any readable embroidery format and returns the
pattern as an instance of pyembroidery.EmbPattern
    Inputs:
        FilePath: Filepath of the embroidery pattern file
    Output:
        Pattern: The embroidery pattern as pyembroidery.EmbPattern instance"""

from __future__ import division
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import pyembroidery

ghenv.Component.Name = "PatternRead"
ghenv.Component.NickName = "PR"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "1 Input/Output"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, FilePath):
        # Initialize output
        Pattern = None

        # only do something if input is defined
        if (FilePath != None and \
        isinstance(FilePath, Grasshopper.DataTree[object]) == True):
            # create empty output tree
            Pattern = Grasshopper.DataTree[object]()
            # loop over all branches
            for i in range(FilePath.BranchCount):
                branchList = FilePath.Branch(i)
                branchPath = FilePath.Path(i)
                # loop over all items in the current branch
                for j in range(branchList.Count):
                    try:
                        ptrn = pyembroidery.read(branchList[j])
                        Pattern.Add(ptrn, branchPath)
                    except:
                        raise RuntimeError("Could not read embroidery file!" + \
                                          "Please check if format is readable.")

        # return outputs if you have them; here I try it for you:
        return Pattern
