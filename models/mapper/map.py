# -*- coding: utf-8 -*-

# USAGE - pvpython map.py DATADIR ORIGINS TARGETS
# EXAMPLE - pvpython view.py output "building1/building2/building3" "water"

from __future__ import division

import vtk,sys
from vtk.util import numpy_support
import numpy as np
import random
import subprocess
from pycaster import pycaster
import shutil,os

class FieldMapper:

    def __init__(self,cfdData,feaMesh,fields):
        self.cfdData = cfdData
        self.feaMesh = feaMesh
        self.fields = fields
        
    def go(self):
        
        print "Mapping",self.cfdData,"to",self.feaMesh
        
        # identify inner wall points

        """
        reader = vtk.vtkSTLReader()
        reader.SetFileName(self.feaMesh)
        reader.ScalarTagsOn()
        reader.Update()
        feadata = reader.GetOutput()
        """
        
        reader = vtk.vtkExodusIIReader()
        reader.SetFileName(self.feaMesh)
        reader.UpdateInformation()
        reader.SetAllArrayStatus(vtk.vtkExodusIIReader.NODAL, 1) # enables all NODAL variables
        reader.GenerateGlobalNodeIdArrayOn()
        reader.GenerateGlobalElementIdArrayOn()
        reader.ExodusModelMetadataOn()
        reader.Update()
        feadata = vtk.vtkCompositeDataGeometryFilter()
        feadata.SetInputConnection(0, reader.GetOutputPort(0))
        feadata.Update()

        transform = vtk.vtkTransform()
        transform.Scale(1000, 1000, 1000)
        test = vtk.vtkTransformPolyDataFilter()
        test.SetTransform(transform)
        test.SetInput(feadata.GetOutput())
        test.Update()
        feadata = test.GetOutput()
        
        normals = vtk.vtkPolyDataNormals()
        normals.SetInput(feadata)
        normals.ComputeCellNormalsOn()
        normals.ComputePointNormalsOn()
        normals.ConsistencyOn()
        normals.AutoOrientNormalsOn()
        normals.SplittingOn()
        normals.Update()
        feabody = normals.GetOutput()
        
        norms = feabody.GetPointData().GetArray('Normals')
        norms_n = numpy_support.vtk_to_numpy(norms)
        #print (norms_n)
        
        feapnts = feabody.GetPoints().GetData()
        feapnts_n = numpy_support.vtk_to_numpy(feapnts)
        #print (feapnts_n)

        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(self.cfdData)
        reader.ReadAllVectorsOn()
        reader.ReadAllScalarsOn()
        reader.Update()
        cfddata = reader.GetOutput()
        
        transform = vtk.vtkTransform()
        transform.Scale(1000, 1000, 1000)
        test = vtk.vtkTransformPolyDataFilter()
        test.SetTransform(transform)
        test.SetInputConnection(reader.GetOutputPort())
        test.Update()
        cfddata = test.GetOutput()
        
        """
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName("volume.vtk")
        reader.ReadAllVectorsOn()
        reader.ReadAllScalarsOn()
        reader.Update()
        cfdvol = reader.GetOutput()
        """ 
       
        cfdpnts = cfddata.GetPoints().GetData()
        cfdpnts_n = numpy_support.vtk_to_numpy(cfdpnts)
        
        pointLocator = vtk.vtkPointLocator()
        pointLocator.SetDataSet(feabody)
        pointLocator.BuildLocator()

        innerIds = []
        for cfdpnt in cfdpnts_n:
            id = pointLocator.FindClosestPoint(cfdpnt)
            innerIds.append(id)
        innerIds = np.unique(innerIds)
            
        # foreach fea innerpoint
        # find the intersection point to cfddata
        # probe field cfddata using intersection point
        # append the field data to feabody
        
        caster = pycaster.rayCaster(cfddata) 
        
        interPoints={}
        interPointsSave = vtk.vtkPoints()
        ptcount=0
        for id in innerIds:
            feainpnt = feapnts_n[id]
            feainnorm = norms_n[id]
            sourcePnt = feainpnt
            targetPnt = feainpnt+(feainnorm*100)
            pointsIntersection = caster.castRay(sourcePnt, targetPnt)
            if len(pointsIntersection)!=0:
                interPointsSave.InsertPoint(ptcount, pointsIntersection[0]+(feainnorm*0))
                interPoints[id]=ptcount
                ptcount+=1
            else:
                targetPnt = feainpnt-(feainnorm*100)
                pointsIntersection = caster.castRay(sourcePnt, targetPnt)
                if len(pointsIntersection)!=0:
                    interPointsSave.InsertPoint(ptcount, pointsIntersection[0]-(feainnorm*0))
                    interPoints[id]=ptcount
                    ptcount+=1

        # for each interPoint, probe cfddata fields

        innerPointData = vtk.vtkPolyData()
        innerPointData.SetPoints(interPointsSave)
        
        """
        # IF LOADING FROM VOLUME
        transform = vtk.vtkTransform()
        transform.Scale(0.001,0.001,0.001)
        test = vtk.vtkTransformPolyDataFilter()
        test.SetTransform(transform)
        test.SetInput(innerPointData)
        test.Update()
        innerPointData = test.GetOutput()
        """
        
        probe = vtk.vtkProbeFilter()
        probe.SetInput(innerPointData)
        probe.SetSource(cfddata)
        
        pd = vtk.vtkAppendPolyData()
        pd.AddInputConnection(probe.GetOutputPort())
        pd.Update()
        probeData=pd.GetOutput()
        
        # detect all fields
        #fields=[]
        #for f in range(0,probeData.GetPointData().GetNumberOfArrays()):
        #    fields.append(probeData.GetPointData().GetArrayName(f))
        
        globalNodeIds=numpy_support.vtk_to_numpy(feabody.GetPointData().GetArray('PedigreeNodeId'))
        
        fieldData={}
        for f in self.fields:
            fieldData[f]=numpy_support.vtk_to_numpy(probeData.GetPointData().GetArray(f))
        
        for f in self.fields:
            ff = open("bc/"+f+"/"+f+"_"+self.cfdData.split("_")[1].replace(".vtk",".inp"),'w')
            if (f == "T"):
                ff.write("*BOUNDARY\n")
            elif (f == "p"):
                ff.write("*CLOAD\n")
            for id in innerIds:
                try:
                    #print ",".join([str(globalNodeIds[id]),'11','11',str(fieldData[f][interPoints[id]])])
                    if fieldData[f][interPoints[id]] != 0:
                        if (f == "T"):
                            ff.write(",".join([str(globalNodeIds[id]),'11','11',str(fieldData[f][interPoints[id]])])+"\n")
                        elif (f == "p"):
                            ff.write(",".join([str(globalNodeIds[id]),'3',str(fieldData[f][interPoints[id]])])+"\n")
                except:
                    pass
            ff.close()
        
        #writer = vtk.vtkDataSetWriter()
        #writer.SetFileName('probe.vtk')
        #writer.SetInput(probe.GetOutput())
        #writer.Write()

        """
        # WRITE INTERSECTION POINTS TO FILE
        interPointsSave = vtk.vtkPoints()
        ptcount=0
        for pnt in interPoints:
            interPointsSave.InsertPoint(ptcount, pnt)
            ptcount+=1
        innerPointData = vtk.vtkPolyData()
        innerPointData.SetPoints(interPointsSave)
        writer = vtk.vtkDataSetWriter()
        writer.SetFileName('points.vtk')
        writer.SetInput(innerPointData)
        writer.Write()
        """

        """
        # INDIVIDUAL POINT TEST
        pSource = [0.01*1000,0.01*1000,0.00125*1000]
        pTarget = [0,0,0.00125*1000]
        pointsIntersection = caster.castRay(pSource, pTarget)
        print pointsIntersection
        
        interPointsSave = vtk.vtkPoints()
        ptcount=0
        for pnt in pointsIntersection:
            interPointsSave.InsertPoint(ptcount, pnt)
            ptcount+=1
        innerPointData = vtk.vtkPolyData()
        innerPointData.SetPoints(interPointsSave)
        writer = vtk.vtkDataSetWriter()
        writer.SetFileName('output.vtk')
        writer.SetInput(innerPointData)
        writer.Write()
        """
        
import re

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    l.sort(key=alphanum_key)
    
runHere=sys.argv[0] == 'map.py'
if (runHere):
    
    print ""
    print "Running Field Mapper..."
    print ""

    cfdMesh = sys.argv[1]
    feaMesh = sys.argv[2]
    fields = ['T']
    
    for f in fields:
        try:
            shutil.rmtree("bc/"+f)
        except:
            pass
        os.mkdir("bc/"+f)
    
    if (os.path.exists(cfdMesh) and os.path.isdir(cfdMesh)):
        # loop through all files
        print "Looping through files..."
        files =  os.listdir(cfdMesh)
        sort_nicely(files)
        for mesh in files:
            FieldMap = FieldMapper(cfdMesh+"/"+mesh,feaMesh,fields)
            FieldMap.go()
    else:
        FieldMap = FieldMapper(cfdMesh,feaMesh,fields)
        FieldMap.go()