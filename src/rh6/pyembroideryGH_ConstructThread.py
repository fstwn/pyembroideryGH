"""Constructs an embroidery thread from its component parts. The thread is
returned as an instance of pyembroidery.EmbThread.
            Inputs:
                ColorRGB: The color of the thread as RGB color (required)
                Description: The color description of the thread (optional)
                CatalogNr: The catalogue number of the thread (optional)
                Details: The details of the thread (optional)
                Brand: The brand of the thread (optional)
                Chart: The chart of the thread (optional)
                Weight: The weight of the thread (optional)
            Output:
                Thread: The newly constructed thread for a stitch/pattern as
                        pyembroidery.EmbThread instance
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
import System.Drawing.Color as SysColor

ghenv.Component.Name = "ConstructThread"
ghenv.Component.NickName = "CT"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "3 Pattern Creation"

__author__ = "Max Eschenbach"
__version__ = "2019.11.04"

class ConThread(component):

    def RunScript(self, ColorRGB, Description, CatalogNr, Details, Brand,
                                                                Chart, Weight):
        # initialize output as empty GH datatree
        Thread = Grasshopper.DataTree[object]()
        
        # abort if no color input is supplied
        if (ColorRGB == None or \
        isinstance(ColorRGB, Grasshopper.DataTree[object]) != True):
            return Thread
        
        # loop through all branches
        for i in range(ColorRGB.BranchCount):
            branchList = ColorRGB.Branch(i)
            branchPath = ColorRGB.Path(i)
            
            # loop through all items in current branch
            for j in range(branchList.Count):
                # create new thread
                thrd = pyembroidery.EmbThread()
                
                # set the color of the newly created thread
                col = branchList[j]
                thrd.set_color(col.R, col.G, col.B)
                
                # look for corresponding data in the other inputs by looking
                # for the exact same path as the ColorRGB-Input
                # COMBINATIONS FOR DESCRIPTION
                if Description.PathExists(branchPath):
                    try:
                        cList = list(Description.Branch(branchPath))
                        thrd.description = cList[j]
                    except IndexError:
                        thrd.description = None
                # COMBINATIONS FOR CATALOG NUMBER
                if CatalogNr.PathExists(branchPath):
                    try:
                        cList = list(CatalogNr.Branch(branchPath))
                        thrd.catalog_number = cList[j]
                    except IndexError:
                        thrd.catalog_number = None
                # COMBINATIONS FOR DETAILS
                if Details.PathExists(branchPath):
                    try:
                        cList = list(Details.Branch(branchPath))
                        thrd.details = cList[j]
                    except IndexError:
                        thrd.details = None
                # COMBINATIONS FOR BRAND
                if Brand.PathExists(branchPath):
                    try:
                        cList = list(Brand.Branch(branchPath))
                        thrd.brand = cList[j]
                    except IndexError:
                        thrd.brand = None
                # COMBINATIONS FOR CHART
                if Chart.PathExists(branchPath):
                    try:
                        cList = list(Chart.Branch(branchPath))
                        thrd.chart = cList[j]
                    except IndexError:
                        thrd.chart = None
                # COMBINATIONS FOR WEIGHT
                if Weight.PathExists(branchPath):
                    try:
                        cList = list(Weight.Branch(branchPath))
                        thrd.weight = cList[j]
                    except IndexError:
                        thrd.weight = None

                # add the thread to the output tree
                Thread.Add(thrd, branchPath)

        # return outputs if you have them; here I try it for you:
        return Thread
