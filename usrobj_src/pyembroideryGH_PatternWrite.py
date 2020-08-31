"""Writes one or many embroidery patterns to one or many files. If multiple
patterns are supplied but only one filepath, only the first pattern will be
written to the file to avoid errors!
            Inputs:
                Pattern: The pattern or many patterns as
                pyembroidery.EmbPattern instance
                FilePath: The Filepath(s) of the file(s) to be written
                Execute: Connect a Boolean Button here, press that button to
                write the files.
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
#import ghpythonlib.treehelpers as th

ghenv.Component.Name = "PatternWrite"
ghenv.Component.NickName = "PW"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "1 Input/Output"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Pattern, FilePath, Execute):

        if Pattern.DataCount != 0 and Pattern.DataCount < 2:
            pattern = Pattern.Branch(0)
            FilePath = str(FilePath[::]).split("\\")
            FilePath = "\\\\".join(FilePath)


            if Execute == True:
                try:
                    pyembroidery.write(pattern[0], FilePath)
                except IndexError:
                    pass
