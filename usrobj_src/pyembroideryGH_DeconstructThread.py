"""Deconstructs a thread by retrieving all of its relevant data.
The thread has to be supplied as an instance of pyembroidery.EmbThread.
            Inputs:
                Thread: The thread of a stitch/pattern as
                        pyembroidery.EmbThread instance
            Output:
                Color: The color of the thread as pyembroidery color string
                ColorRGB: The color of the thread as System.Color RGB Color
                Description: The description of the thread
                CatalogNr: The catalogue number of the thread
                Details: The details of the thread
                Brand: The brand of the thread
                Chart: The chart of the thread
                Weight: The weight of the thread
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
import System.Drawing.Color as SysColor
import pyembroidery

ghenv.Component.Name = "DeconstructThread"
ghenv.Component.NickName = "DT"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "2 Pattern Analysis"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class MyComponent(component):

    def RunScript(self, Thread):
        # initialize outputs
        Color = None
        ColorRGB = None
        Description = None
        CatalogNr = None
        Details = None
        Brand = None
        Chart = None
        Weight = None

        # only execute if there is a thread supplied to begin with
        if (Thread != None and \
        isinstance(Thread, Grasshopper.DataTree[object]) == True):
            # if the tree has more than one path it is a "real" tree
            if len(list(Thread.Paths)) >= 1:
                # initialize ouputs as DataTrees
                Color = Grasshopper.DataTree[object]()
                ColorRGB = Grasshopper.DataTree[object]()
                Description = Grasshopper.DataTree[object]()
                CatalogNr = Grasshopper.DataTree[object]()
                Details = Grasshopper.DataTree[object]()
                Brand = Grasshopper.DataTree[object]()
                Chart = Grasshopper.DataTree[object]()
                Weight = Grasshopper.DataTree[object]()

               # loop over branches of original tree
                for i in range(Thread.BranchCount):
                    branchList = Thread.Branch(i)
                    branchPath = Thread.Path(i)

                    # loop over all items of original tree,
                    # extract data and add to output trees
                    for j in range(branchList.Count):
                        Color.Add(branchList[j].color, branchPath)
                        ColorRGB.Add(SysColor.FromArgb(255,
                                                      branchList[j].get_red(),
                                                      branchList[j].get_green(),
                                                      branchList[j].get_blue()),
                                                      Thread.Path(i))
                        Description.Add(branchList[j].description, branchPath)
                        CatalogNr.Add(branchList[j].catalog_number, branchPath)
                        Details.Add(branchList[j].details, branchPath)
                        Brand.Add(branchList[j].brand, branchPath)
                        Chart.Add(branchList[j].chart, branchPath)
                        Weight.Add(branchList[j].weight, branchPath)

        # return outputs if you have them; here I try it for you:
        return (ColorRGB, Description, CatalogNr, Details, Brand, Chart, Weight)
