"""
Deconstructs a thread by retrieving all of its relevant data.
The thread has to be supplied as an instance of pyembroidery.EmbThread.
    Inputs:
        Thread: The thread of a stitch/pattern as an instance of
                pyembroidery.EmbThread.
                {tree, EmbThread}
    Output:
        ColorRGB: The color of the thread as a System.Drawing.Color RGB Color.
                  {tree, System.Drawing.Color}
        Description: The color of the thread as pyembroidery color string.
                     {tree, str}
        CatalogNr: The catalogue number of the thread.
                   {tree, int}
        Details: The details of the thread if present, otherwise Null.
                 {tree, ?}
        Brand: The brand of the thread if present, othwerise Null.
               {tree, str}
        Chart: The chart of the thread if present, otherwise Null.
               {tree, string}
        Weight: The weight of the thread if present, otherwise Null.
                {tree, ?}
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

# THIRD PARTY MODULE IMPORTS
import System.Drawing.Color as SysColor

# GHENV COMPONENT SETTINGS 
ghenv.Component.Name = "DeconstructThread"
ghenv.Component.NickName = "DT"
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

class DeconstructThread(component):
    
    def RunScript(self, ThreadTree):
        # initialize ouputs as DataTrees
        ColorRGB = Grasshopper.DataTree[object]()
        Description = Grasshopper.DataTree[object]()
        CatalogNr = Grasshopper.DataTree[object]()
        Details = Grasshopper.DataTree[object]()
        Brand = Grasshopper.DataTree[object]()
        Chart = Grasshopper.DataTree[object]()
        Weight = Grasshopper.DataTree[object]()
        
        # only execute if there is a thread supplied to begin with
        if ThreadTree != None and ThreadTree.DataCount:
           # loop over branches of the thread tree
            for i, branch in enumerate(ThreadTree.Branches):
                branch_path = ThreadTree.Path(i)
                
                # loop over all items in branch
                for j, thread in enumerate(branch):
                    if isinstance(thread, pyembroidery.EmbThread):
                        ColorRGB.Add(SysColor.FromArgb(255,
                                                      thread.get_red(),
                                                      thread.get_green(),
                                                      thread.get_blue()),
                                                      branch_path)
                        Description.Add(thread.description, branch_path)
                        CatalogNr.Add(thread.catalog_number, branch_path)
                        Details.Add(thread.details, branch_path)
                        Brand.Add(thread.brand, branch_path)
                        Chart.Add(thread.chart, branch_path)
                        Weight.Add(thread.weight, branch_path)
                    else:
                        rml = self.RuntimeMessageLevel.Warning
                        errMsg = ("Thread '{}' at branch {}, index {} " +
                                  "is not a valid instance of " +
                                  "pyembroidery.EmbThread! A Null item will " +
                                  "be inserted into the output tree!")
                        errMsg = errMsg.format(thread, i, j)
                        self.AddRuntimeMessage(rml, errMsg)
                        ColorRGB.Add(None, branch_path)
                        Description.Add(None, branch_path)
                        CatalogNr.Add(None, branch_path)
                        Details.Add(None, branch_path)
                        Brand.Add(None, branch_path)
                        Chart.Add(None, branch_path)
                        Weight.Add(None, branch_path)
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = "Input Thread failed to collect data!"
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return ColorRGB, Description, CatalogNr, Details, Brand, Chart, Weight
