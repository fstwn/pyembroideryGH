"""
Render an embroidery pattern to the Rhino viewport.
    Inputs:
        Pattern: The embroidery patter to render.
                 {item, EmbPattern}
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 211129
"""
# PYTHON STANDARD LIBRARY IMPORTS
from __future__ import division
from collections import deque

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "RenderPattern"
ghenv.Component.NickName = "RP"
ghenv.Component.Category = "pyembroideryGH"
ghenv.Component.SubCategory = "5 Display & Preview"

# LOCAL MODULE IMPORTS
try:
    import pyembroidery
except ImportError:
    errMsg = ("The pyembroidery python module seems to be not correctly " +
              "installed! Please make sure the module is in you search " +
              "path, see README for instructions!.")
    raise ImportError(errMsg)

class RenderPattern(component):
    
    def __init__(self):
        super(RenderPattern, self).__init__()
        self.drawing_curves = []
    
    def get_ClippingBox(self):
        return Rhino.Geometry.BoundingBox()
    
    def DrawViewportWires(self, args):
        try:
            # get display from args
            display = args.Display
            
            # draw all catalogued curves
            for crv in self.drawing_curves:
                display.DrawCurve(crv[0].ToNurbsCurve(), crv[1], 2)
        
        except Exception, e:
            System.Windows.Forms.MessageBox.Show(str(e),
                                                 "Error while drawing preview!")
    
    def RunScript(self, Pattern):
        
        # INITIALIZATION ------------------------------------------------------
        
        if Pattern:
            # split the pattern into colorblocks
            PCB = list(Pattern.get_as_colorblocks())
            
            simulation_pts = []
            simulation_curves = []
            
            # loop through all colorblocks
            for i, cb in enumerate(PCB):
                """
                if i > 0:
                    break
                """
                stitches = cb[0]
                thread = cb[1]
                color = System.Drawing.Color.FromArgb(thread.get_red(),
                                                      thread.get_green(),
                                                      thread.get_blue())
                
                # loop over all stitches in the colorblock
                simcrv = Rhino.Geometry.Polyline()
                for j, stitch in enumerate(stitches):
                    pt = Rhino.Geometry.Point3d(stitch[0] * 0.1, stitch[1] * -0.1, 0)
                    cmd = stitch[2]
                    
                    """
                    if cmd != 0:
                        print cmd
                    """
                    
                    # if no command, continue
                    if cmd == -1:
                        continue
                    # add point and end curve on trim command
                    if cmd == 2:
                        # trim at this coordinate and begin a new curve
                        simcrv.Add(pt)
                        simulation_curves.append((simcrv, color))
                        simcrv = Rhino.Geometry.Polyline()
                    # end curve on color break command
                    elif cmd == 226:
                        continue
                        simulation_curves.append((simcrv, color))
                        simcrv = Rhino.Geometry.Polyline()
                    # normal operation, ad points to the curve
                    else:
                        simcrv.Add(pt)
                        if j == len(stitches) - 1:
                            simulation_curves.append((simcrv, color))
            
            self.drawing_curves = simulation_curves
        
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Input Pattern failed to collect data!")
            self.AddRuntimeMessage(rml, errMsg)
            self.drawing_curves = []
