# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.2.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/marmar/scratch/parallelWorks/heatTransfer/workflow_DEX_fixedPoints/models/mesh')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_1 = geompy.MakeBoxDXDYDZ(0.01, 0.0125, 0.003)
geomObj_2 = geompy.MakeTranslation(geomObj_1, -0.005, -0.00625, 0)
[geomObj_3,geomObj_4,geomObj_5,geomObj_6,geomObj_7,geomObj_8] = geompy.ExtractShapes(geomObj_2, geompy.ShapeType["FACE"], True)
geomObj_9 = geompy.MakePrismVecH(geomObj_3, OX, 0.00025)
geomObj_10 = geompy.MakePrismVecH(geomObj_4, OY, 0.00025)
geomObj_11 = geompy.MakePrismVecH(geomObj_7, OY, -0.00025)
geomObj_12 = geompy.MakePrismVecH(geomObj_8, OX, -0.00025)
geomObj_13 = geompy.MakePrismVecH(geomObj_6, OZ, -0.00025)
geomObj_14 = geompy.MakePrismVecH(geomObj_5, OZ, 0.00025)
geomObj_15 = geompy.MakeFuseList([geomObj_9, geomObj_10, geomObj_11, geomObj_12, geomObj_13, geomObj_14], True, True)
geomObj_16 = geompy.MakeCircle(O, OY, 0.000625)
geomObj_17 = geompy.MakeCircle(O, OY, 0.0005)
geomObj_18 = geompy.MakeFaceWires([geomObj_16, geomObj_17], 1)
geomObj_19 = geompy.MakeTranslation(geomObj_18, 0, 0.006, 0.0015)
geomObj_20 = geompy.MakePrismVecH(geomObj_19, OY, 0.00125)
Extrusion_7a = geompy.MakeTranslation(geomObj_20, -0.00175, 0, 0)
geomObj_21 = geompy.MakeCircle(O, OY, 0.00125)
geomObj_22 = geompy.MakeCircle(O, OY, 0.001)
geomObj_23 = geompy.MakeFaceWires([geomObj_21, geomObj_22], 1)
geomObj_24 = geompy.MakeTranslation(geomObj_23, 0, -0.006, 0.0015)
geomObj_25 = geompy.MakePrismVecH(geomObj_24, OY, -0.00125)
Extrusion_8a = geompy.MakeTranslation(geomObj_25, 0.00175, 0, 0)
geomObj_26 = geompy.MakeCutList(geomObj_15, [Extrusion_7a, Extrusion_8a], True)
[geomObj_27,Solid_2,geomObj_28] = geompy.ExtractShapes(geomObj_26, geompy.ShapeType["SOLID"], True)
[geomObj_29,geomObj_30,geomObj_31] = geompy.ExtractShapes(geomObj_27, geompy.ShapeType["FACE"], True)
[geomObj_32,geomObj_33,geomObj_34] = geompy.ExtractShapes(geomObj_28, geompy.ShapeType["FACE"], True)
heatSource = geompy.MakeBoxDXDYDZ(0.002, 0.003, 0.001)
heatSource_1 = geompy.MakeTranslation(heatSource, 0.001, -0.0025, 0.00025)
Fuse_2 = geompy.MakeFuseList([Extrusion_7a, Extrusion_8a, Solid_2, heatSource_1], True, True)
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["VERTEX"])
geomObj_35 = geompy.MakeTranslation(geomObj_31, 0, 0.001, 0)
geomObj_36 = geompy.MakeTranslation(geomObj_32, 0, -0.001, 0)
geompy.ExportSTL(Fuse_2, "meshHS.unv", False, 0.001, True)
geompy.ExportSTL(geomObj_35, "meshHS.unv", False, 0.001, True)
geompy.ExportSTL(geomObj_36, "meshHS.unv", False, 0.001, True)
FixedLine = geompy.CreateGroup(Fuse_2, geompy.ShapeType["EDGE"])
geompy.UnionIDs(FixedLine, [32, 17])
inletSurface = geompy.CreateGroup(Fuse_2, geompy.ShapeType["FACE"])
geompy.UnionIDs(inletSurface, [66])
geompy.ExportSTL(Fuse_2, "meshHS.unv", False, 0.001, True)
geompy.ExportSTL(Fuse_2, "/home/marmar/scratch/parallelWorks/heatTransfer/workflow_DEX_fixedPoints/models/mesh/Fuse_2.stl", True, 0.001, True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Extrusion_7a, 'Extrusion_7a' )
geompy.addToStudy( Extrusion_8a, 'Extrusion_8a' )
geompy.addToStudy( Solid_2, 'Solid_2' )
geompy.addToStudy( heatSource, 'heatSource' )
geompy.addToStudy( heatSource_1, 'heatSource_1' )
geompy.addToStudy( Fuse_2, 'Fuse_2' )
geompy.addToStudyInFather( Fuse_2, FixedLine, 'FixedLine' )
geompy.addToStudyInFather( Fuse_2, inletSurface, 'inletSurface' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Fuse_2)
Regular_1D = Mesh_1.Segment()
MaxLength_0_0004 = Regular_1D.MaxSize(0.0004)
MEFISTO_2D = Mesh_1.Triangle(algo=smeshBuilder.MEFISTO)
NETGEN_3D = Mesh_1.Tetrahedron()
isDone = Mesh_1.Compute()
FixedLine_1 = Mesh_1.GroupOnGeom(FixedLine,'FixedLine',SMESH.EDGE)
inletSurface_1 = Mesh_1.GroupOnGeom(inletSurface,'inletSurface',SMESH.FACE)
FixedLine_2 = Mesh_1.GroupOnGeom(FixedLine,'FixedLine',SMESH.NODE)
inletSurface_2 = Mesh_1.GroupOnGeom(inletSurface,'inletSurface',SMESH.NODE)
try:
  Mesh_1.ExportUNV( r'meshHS.unv' )
except:
  print 'ExportUNV() failed. Invalid file name?'


## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
smesh.SetName(MEFISTO_2D.GetAlgorithm(), 'MEFISTO_2D')
smesh.SetName(MaxLength_0_0004, 'MaxLength=0.0004')
smesh.SetName(inletSurface_1, 'inletSurface')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(FixedLine_1, 'FixedLine')
smesh.SetName(inletSurface_2, 'inletSurface')
smesh.SetName(FixedLine_2, 'FixedLine')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
