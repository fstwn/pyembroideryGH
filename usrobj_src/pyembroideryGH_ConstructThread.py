"""
Constructs an embroidery thread from its component parts. The thread is
returned as an instance of pyembroidery.EmbThread.
    Inputs:
        ColorRGB: The color of the thread as RGB color (required).
                  {item, System.Drawing.Color}
        Description: The color description of the thread (optional).
                     {item, str}
        CatalogNr: The catalogue number of the thread (optional).
                   {item, str}
        Details: The details of the thread (optional).
                 {item, str}
        Brand: The brand of the thread (optional).
               {item, str}
        Chart: The chart of the thread (optional).
               {item, str}
        Weight: The weight of the thread (optional).
                {item, str}
    Output:
        Thread: The newly constructed thread for a stitch/pattern as
                pyembroidery.EmbThread instance.
                {item/list/tree, EmbThread}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 201022
"""

# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# ADDITIONAL RHINO AND SYSTEM IMPORTS
import System.Drawing.Color as SysColor

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "ConstructThread"
ghenv.Component.NickName = "CT"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

class ConstructThread(component):

    def RunScript(self, ColorRGB, Description, CatalogNr, Details, Brand, Chart, Weight):
        # initialize output as empty GH datatree
        Thread = Grasshopper.DataTree[object]()
        
        if ColorRGB:
            # create new thread
            Thread = pyembroidery.EmbThread()
            # set the color of the newly created thread
            Thread.set_color(ColorRGB.R, ColorRGB.G, ColorRGB.B)
            # set the other data to the thread if present
            Thread.description = Description
            Thread.catalog_number = CatalogNr
            Thread.details = Details
            Thread.brand = Brand
            Thread.chart = Chart
            Thread.weight = Weight
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = "Input ColorRGB failed to collect data!"
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return Thread
