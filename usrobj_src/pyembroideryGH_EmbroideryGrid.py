"""
Create grid-based embroidery stitches inside a closed boundary (closed curve).
    Inputs:
        Pattern: List of curves to create grid-based embroidery inside.
                 {list, Curve}
        ResolutionX: Resolution of stitches in X direction of the supplied
                     plane.
                     {item, float}
        ResolutionY: Resolution of stitches in Y direction of the supplied
                     plane.
                     {item, float}
        StitchPlane: Plane for creating the grid based embroidery stitches.
                     {item, Plane}
        Thread: EmbThread to use for the grid-based embroidery.
                {item, EmbThread}
    Output:
        StitchPts: The stitch points of the generated embroidery as Rhino 
                   Points.
                   {list/tree, Point3d}
        Stitches: The stitches of the generated embroidery in string format.
                  {list/tree, str)
        StitchBlock: The generated grid-based embroidery as a StitchBlock.
                     {item/list/tree, SitchBlock)
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

# ADDITIONAL RHINO IMPORTS
import scriptcontext
from ghpythonlib import treehelpers as th

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "EmbroideryGrid"
ghenv.Component.NickName = "EG"
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

class EmbroideryGrid(component):
    
    def _sanitize_input_data(self, crvs, planes, threads):
        # get longest list
        data = [crvs, planes, threads]
        counts = [len(l) for l in data]
        maxcount = max(counts)
        for i in range(maxcount):
            if i > len(crvs) - 1:
                crvs.append(crvs[-1])
            if i > len(planes) - 1:
                planes.append(planes[-1])
            if i > len(threads) - 1:
                threads.append(threads[-1])
        return crvs, planes, threads
    
    def _get_branch_counts(self, branched_rows):
        return [len(row) for row in branched_rows] 
    
    def _get_first_nonzero(self, branched_rows):
        for i, row in enumerate(branched_rows):
            if len(row) > 0:
                return i
        return -1
    
    def _point_to_stitch(self, pt, cmd):
        return ",".join([str(pt.X * 10), 
                         str(pt.Y * -10),
                         str(cmd)])
    
    def _points_to_stitches(self, pts, cmds):
        stitches = []
        stitch_strings = []
        if len(pts) >= len(cmds):
            for i, pt in enumerate(pts):
                # extract command with failsafe
                if i <= len(cmds) - 1:
                    command = cmds[i]
                else:
                    command = cmds[-1]
                # compile stitch string
                stitch_str = ",".join([str(pt.X * 10), 
                                       str(pt.Y * -10),
                                       str(command)])
                # append to list of stitches
                stitches.append((pt.X * 10, pt.Y * -10, int(command)))
                stitch_strings.append(stitch_str)
        # list of commands is longer than list of points, so we have to
        # loop over the list of commands
        elif len(pts) < len(cmds):
            for j, command in enumerate(cmds):
                # extract coordinate with failsafe
                if j <= len(pts) - 1:
                    pt = pts[j]
                else:
                    pt = pts[-1]
                # compile stitch string
                stitch_str = ",".join([str(pt.X * 10),
                                       str(pt.Y * -10),
                                       str(command)])
                # append to list of stitches
                stitches.append((pt.X * 10, pt.Y * -10, int(command)))
                stitch_strings.append(stitch_str)
        return stitches, stitch_strings
    
    def _find_closest_branch(self, lastpt, gridlines, branched_rows):
        candidate_branches = []
        for i, row in enumerate(branched_rows):
            row = branched_rows[i]
            branchcount = len(row)
            if branchcount > 0:
                for j, branch in enumerate(row):
                    dist = lastpt.DistanceToSquared(gridlines[j].PointAt(branch[0]))
                    candidate_branches.append((dist, i, j))
        dists, rowindex, branchindex = zip(*sorted(candidate_branches))
        return (rowindex[0], branchindex[0])
    
    def RunScript(self, input_curves, ResolutionX, ResolutionY, StitchPlane, Thread):
        # initialize outputs so they're never empty
        StitchPts = Grasshopper.DataTree[object]()
        Stitches = Grasshopper.DataTree[object]()
        stitch_block = Grasshopper.DataTree[object]()
        allrows = Grasshopper.DataTree[object]()
        
        # set constants and defaults
        tol = scriptcontext.doc.ModelAbsoluteTolerance
        if not StitchPlane:
            StitchPlane = [Rhino.Geometry.Plane.WorldXY]
        if not Thread:
            Thread = [pyembroidery.EmbThread()]
        
        
        if input_curves and StitchPlane and Thread:
            # sanitize input data list lengths
            input_curves, StitchPlane, Thread = self._sanitize_input_data(input_curves, StitchPlane, Thread)
            
            # CREATE VALID ROWS OF STITCHPTS ----------------------------------
            
            # loop over all input curves
            for i, crv in enumerate(input_curves):
                # first get the boundingbox of the current curve
                bbx = crv.GetBoundingBox(False)
                # then rotate the plane
                bbx_center = Rhino.Geometry.Point3d(bbx.Center.X,
                                                    bbx.Center.Y,
                                                    0.0)
                # get aligned rotated bbx
                pln = StitchPlane[i]
                pln.Origin = bbx_center
                bbx = crv.GetBoundingBox(pln)
                # get projected corners from bounding box
                botleft = pln.PointAt(bbx.Min.X, bbx.Min.Y, bbx.Min.Z)
                botright = pln.PointAt(bbx.Max.X, bbx.Min.Y, bbx.Min.Z)
                topleft = pln.PointAt(bbx.Min.X, bbx.Max.Y, bbx.Min.Z)
                topright = pln.PointAt(bbx.Max.X, bbx.Max.Y, bbx.Min.Z)
                
                # first get all "x axis lines along y" by creating the y
                # axis and dividing it
                y_ax = Rhino.Geometry.LineCurve(botleft, topleft)
                y_basepts = [y_ax.PointAt(t) for t 
                             in y_ax.DivideByCount(ResolutionY, True)]
                tvecs = [Rhino.Geometry.Vector3d(bpt - botleft)
                         for bpt in y_basepts]
                
                # create base x axis
                x_ax = Rhino.Geometry.LineCurve(botleft, botright)
                x_basepts = [x_ax.PointAt(t) for t 
                             in x_ax.DivideByCount(ResolutionX, True)]
                
                # create rows by translating base x axis with all y vectors
                rows = []
                gridlines = []
                gridparams = []
                for v in tvecs:
                    row = [xpt + v for xpt in x_basepts]
                    ln = Rhino.Geometry.Line(row[0], row[-1])
                    gridparams.append([ln.ClosestParameter(pt) for pt in row])
                    ln = ln.ToNurbsCurve()
                    ln.Domain = Rhino.Geometry.Interval(0, 1)
                    rows.append(row)
                    gridlines.append(ln)
                
                # GET INTERSECTION EVENTS AND BRANCHED ROWS -------------------
                
                branched_rows = [deque([]) for x in rows]
                for j, row in enumerate(rows):
                    
                    # get intersection events and all their parameters
                    intevents = Rhino.Geometry.Intersect.Intersection.CurveCurve(gridlines[j], crv, tol, tol)
                    intparams = []
                    for e in intevents:
                        if e.IsOverlap:
                            intparams.append(e.OverlapA.Min)
                            intparams.append(e.OverlapA.Max)
                        else:
                            intparams.append(e.ParameterA)
                    
                    # ONE event means intersection is exactly at a corner
                    # create a new branch with a single point in this row
                    if len(intparams) == 1:
                        branched_rows[j].append(intparams)
                    
                    # >= TWO and EVEN number of intersections means there
                    # are defined domains of points inside the curve
                    elif len(intparams) >= 2 and (len(intparams) % 2) == 0:
                        for k in range(len(intparams)):
                            if k % 2 != 0:
                                continue
                            sequence = [t for t in gridparams[j] if t > intparams[k] and t < intparams[k + 1]]
                            sequence.insert(0, intparams[k])
                            sequence.append(intparams[k + 1])
                            branched_rows[j].append(sequence)
                    
                    # >= THREE and UNEVEN number of intersections means we have
                    # to check point containment to find the domains inside
                    # the boundary curve
                    elif len(intparams) > 2 and (len(intparams) % 2) != 0:
                        protoseq = intparams + [t for t in gridparams[j] if t > min(intparams) and t < max(intparams)]
                        protoseq.sort()
                        last_inside = None
                        sequence = []
                        for k, param in enumerate(protoseq):
                            pt = gridlines[j].PointAt(param)
                            # check point for containment
                            containment =  crv.Contains(pt,
                                                        Rhino.Geometry.Plane.WorldXY,
                                                        tol)
                            pt_on_curve = (containment == Rhino.Geometry.PointContainment.Inside or containment == Rhino.Geometry.PointContainment.Coincident)
                            # if point is in, it is part of the current seq
                            if pt_on_curve:
                                sequence.append(param)
                            elif not pt_on_curve and len(sequence) > 0:
                                branched_rows[j].append(sequence)
                                sequence = []
                            # set boolean to check previous point containment
                            last_inside = pt_on_curve
                
                # LOOP OVER ALL BRANCHED ROWS AND RESOLVE ---------------------
                
                j = 0
                lastidx = -1
                lastcount = 0
                param_sequence = []
                total_sequence = []
                stitch_sequence = []
                block = []
                
                while j < len(branched_rows):
                    # set row and get branchcount
                    row = branched_rows[j]
                    branchcount = len(row)
                    # only step into row if it has any branches
                    if branchcount >= 1:
                        # pop the next branch from the current row
                        branch = row.popleft()
                        stitchpts = [gridlines[j].PointAt(t) for t in branch]
                        commands = [pyembroidery.STITCH for pt in stitchpts]
                        # check for jumps
                        if lastidx != j - 1:
                            print "Jump detected! From {} to {}!".format(lastidx, j)
                            # inject trim command
                            branch.insert(0, param_sequence[-1])
                            stitchpts.insert(0, total_sequence[-1])
                            commands.insert(0, pyembroidery.TRIM)
                            
                            """
                            # if a jump is detected, prepare the travel path
                            spt = gridlines[j].PointAt(param_sequence[-1])
                            ept = gridlines[j].PointAt(branch[0])
                            rawmove = Rhino.Geometry.LineCurve(spt, ept)
                            rawmove.Domain = Rhino.Geometry.Interval(0, 1)
                            # check raw move for intersection
                            intevents = Rhino.Geometry.Intersect.Intersection.CurveCurve(rawmove, crv, tol, tol)
                            intparams = []
                            for e in intevents:
                                if e.IsOverlap:
                                    intparams.append(e.OverlapA.Min)
                                    intparams.append(e.OverlapA.Max)
                                else:
                                    intparams.append(e.ParameterA)
                            print intparams
                            """
                        stitches, stitch_strings = self._points_to_stitches(stitchpts, commands)
                        block.extend(stitches)
                        stitch_sequence.extend(stitch_strings)
                        param_sequence.extend(branch)
                        total_sequence.extend(stitchpts)
                        if j == len(branched_rows) - 1:
                            nzi = self._get_first_nonzero(branched_rows)
                            print "Last row reached, first nonzero is: {}".format(nzi)
                            if nzi != -1:
                                cb = self._find_closest_branch(stitchpts[-1],
                                                               gridlines,
                                                               branched_rows)
                                print cb
                                lastidx = j
                                j = cb[0]
                                continue
                            else:
                                # inject trim and finish
                                stitch = block[-1]
                                stitch = (stitch[0], stitch[1], pyembroidery.TRIM)
                                block.append(stitch)
                                stitch_strings.append(",".join([str(stitch[0]), 
                                                                str(stitch[1]),
                                                                str(stitch[2])]))
                                param_sequence.append(param_sequence[-1])
                                total_sequence.append(total_sequence[-1])
                                break
                    
                    # if row is empty, find nonzero row with the lowest index
                    else:
                        nzi = self._get_first_nonzero(branched_rows)
                        print "Row at index {} has no branches! First nonzero is: {}".format(j, nzi)
                        if nzi != -1:
                            lastidx = j
                            j = nzi
                            continue
                        # if all rows are empty, inject trim command and finish
                        else:
                            stitch = block[-1]
                            stitch = (stitch[0], stitch[1], pyembroidery.TRIM)
                            block.append(stitch)
                            stitch_strings.append(",".join([str(stitch[0]), 
                                                            str(stitch[1]),
                                                            str(stitch[2])]))
                            param_sequence.append(param_sequence[-1])
                            total_sequence.append(total_sequence[-1])
                            lastidx = j
                            j += 1
                            break
                    
                    # set last index value and increment j
                    lastidx = j
                    j += 1
                
                # CREATE STITCHBLOCK ------------------------------------------
                
                try:
                    sblock = StitchBlock(block, Thread[i])
                except Exception, e:
                    rml = self.RuntimeMessageLevel.Warning
                    errMsg = "Could not create StitchBlock at index {}!"
                    errMsg = " ".join([errMsg, e]).format(i)
                    self.AddRuntimeMessage(rml, errMsg)
                    sblock = None
                
                # PREPARE OUTPUTS ---------------------------------------------
                path = Grasshopper.Kernel.Data.GH_Path(i)
                StitchPts.AddRange(total_sequence, path)
                Stitches.AddRange(stitch_sequence, path)
                stitch_block.Add(sblock, path)
                
                # dev output
                for j, row in enumerate(rows):
                    allrows.AddRange(row, path)
            
        else:
            rml = self.RuntimeMessageLevel.Warning
            errMsg = ("Input Curve failed to collect data!")
            self.AddRuntimeMessage(rml, errMsg)
        
        # return outputs if you have them; here I try it for you:
        return StitchPts, Stitches, stitch_block