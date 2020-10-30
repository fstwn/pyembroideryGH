"""
Writes one or many embroidery patterns to one or many files. If multiple
patterns are supplied but only one filepath, additional filepaths in the
same folder with the indices of the pattern as suffix will be created!
---
Supported file formats are:
*.pec, *.pes, *.exp, *.dst, *.jef, *.vp3, *.csv, *.xxx, *.sew, *.u01, *.shv,
*.10o, *.100, *.bro, *.dat, *.dsb, *.dsz, *.emd, *.exy, *.fxy, *.gt, *.inb,
*.tbf, *.ksm, *.tap, *.stx, *.phb, *.phc, *.new, *.max, *.mit, *.pcd, *.pcq,
*.pcm, *.pcs, *.jpx, *.stc, *.zxy, *.pmv, *.png, *.txt, *.gcode, *.hus, *.edr,
*.col, *.inf, *.json
    Inputs:
        Pattern: One or several embroidery patterns as pyembroidery.EmbPattern 
                 instances.
                 {item, EmbPattern}
        FilePath: The Filepath(s) of the file(s) to be written
        Execute: Connect a Boolean Button here, press that button to
        write the files.
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201030
"""

# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division
from os import path

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# ADDITIONAL RHINO IMPORTS
from scriptcontext import sticky as st

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "PatternWrite"
ghenv.Component.NickName = "PW"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "1 Input/Output"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class PatternWrite(component):
    
    def RunScript(self, Pattern, FilePath, Execute):
        # check supported formats
        supported = [d["extension"] for d in pyembroidery.supported_formats()]
        supported = ["." + ext for ext in supported]
        supported = {ext : True for ext in supported}
        
        # verify pattern and filepaths
        if Pattern and FilePath:
            # make info message
            if len(Pattern) > len(FilePath):
                rml = self.RuntimeMessageLevel.Remark
                imsg = ("List of supplied filepaths does not suffice. " +
                        "Additional filepaths will be constructed based on " +
                        "the last one to write all patterns!")
                self.AddRuntimeMessage(rml, imsg)
            
            # loop over patterns and verify/construct filepaths
            for i, pat in enumerate(Pattern):
                # if there is a valid supplied filepath
                if i <= len(FilePath) -1:
                    # normalize path and get extension
                    fp = path.normpath(FilePath[i].strip("\n\r"))
                    ext = path.splitext(fp)[1]
                    # if format in not supported, add warning
                    if ext not in supported:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("Format with extension '{}' is not a " + 
                                  "supported file format! Please check the " + 
                                  "description for a list of supported " +
                                  "formats. This pattern will not be written!")
                        errMsg = errMsg.format(ext)
                        self.AddRuntimeMessage(rml, errMsg)
                        continue
                else:
                    fp = path.normpath(FilePath[-1].strip("\n\r"))
                    fp, ext = path.splitext(fp)
                    # if format in not supported, add warning
                    if ext not in supported:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("Format with extension '{}' is not a " + 
                                  "supported file format! Please check the " + 
                                  "description for a list of supported " +
                                  "formats. This pattern will not be written!")
                        errMsg = errMsg.format(ext)
                        self.AddRuntimeMessage(rml, errMsg)
                        continue
                    # alter filepath to avoid overwriting original files
                    fp = fp + " ({})"
                    fp = fp.format(i - len(FilePath) + 1) + ext
                
                # write on execute
                if Execute:
                    pyembroidery.write(pat, fp)
        else:
            rml = self.RuntimeMessageLevel.Warning
            if not Pattern: 
                errMsg = "Input Pattern failed to collect data!"
                self.AddRuntimeMessage(rml, errMsg)
            if not FilePath:
                errMsg = "Input FilePath failed to collect data!"
                self.AddRuntimeMessage(rml, errMsg)
