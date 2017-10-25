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
plate = geompy.MakeBoxDXDYDZ(0.008, 0.01, 0.0005)
plate_1 = geompy.MakeTranslation(plate, -0.004, -0.005, 0.00025)
heatSource = geompy.MakeBoxDXDYDZ(0.002, 0.003, 0.001)
heatSource_1 = geompy.MakeTranslation(heatSource, 0.001, -0.0025, 0.00075)
Fuse_2 = geompy.MakeFuseList([Extrusion_7a, Extrusion_8a, Solid_2], True, True)
geomObj_35 = geompy.MakeTranslation(geomObj_31, 0, 0.001, 0)
geomObj_36 = geompy.MakeTranslation(geomObj_32, 0, -0.001, 0)
geompy.ExportSTL(Fuse_2, "meshTest.unv", False, 0.001, True)
geompy.ExportSTL(geomObj_35, "meshTest.unv", False, 0.001, True)
geompy.ExportSTL(geomObj_36, "meshTest.unv", False, 0.001, True)
Compound_1 = geompy.MakeCompound([heatSource_1, plate_1, Fuse_2])
Partition_1 = geompy.MakePartition([Compound_1], [], [], [], geompy.ShapeType["SOLID"], 0, [], 1)
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["SOLID"])
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["EDGE"])
heatSourceSolid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(heatSourceSolid, [2])
[geomObj_37,geomObj_38,geomObj_39,geomObj_40,geomObj_41,geomObj_42] = geompy.SubShapeAll(heatSourceSolid, geompy.ShapeType["FACE"])
[geomObj_43,geomObj_44,geomObj_45,geomObj_46,geomObj_47,geomObj_48] = geompy.SubShapeAll(heatSourceSolid, geompy.ShapeType["FACE"])
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_37)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_38)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_39)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_40)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_41)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_42)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_43)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_44)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_45)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_46)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_47)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_48)
plateSolid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(plateSolid, [36])
BoxOuterFaces = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(BoxOuterFaces, [21, 14, 34, 31, 4])
PlateUpperFace = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(PlateUpperFace, [55])
FixedLine = geompy.CreateGroup(Partition_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(FixedLine, [102])
inletSurface = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(inletSurface, [136])
AllFaces = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(AllFaces, [4, 14, 21, 26, 31, 34, 38, 48, 55, 61, 66, 69, 73, 83, 93, 98, 106, 109, 111, 116, 121, 126, 131, 136, 141, 152, 163, 168, 171, 174])
HeatFluxFaces = geompy.UnionListOfGroups([BoxOuterFaces, PlateUpperFace])
ZeroFluxFaces0 = geompy.CutListOfGroups([AllFaces], [HeatFluxFaces])
BoxPlateInterface = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(BoxPlateInterface, [26])
ZeroFluxFaces = geompy.CutListOfGroups([ZeroFluxFaces0], [BoxPlateInterface])
geompy.ExportSTL(ZeroFluxFaces, "/home/marmar/scratch/parallelWorks/heatTransfer/workflow_DEX_fixedPoints/models/mesh/ZeroFluxFaces.stl", True, 0.001, True)
geompy.ExportSTL(ZeroFluxFaces, "ZeroFluxFaces_test.stl", True, 0.001, True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Extrusion_7a, 'Extrusion_7a' )
geompy.addToStudy( Extrusion_8a, 'Extrusion_8a' )
geompy.addToStudy( Solid_2, 'Solid_2' )
geompy.addToStudy( plate, 'plate' )
geompy.addToStudy( plate_1, 'plate_1' )
geompy.addToStudy( heatSource, 'heatSource' )
geompy.addToStudy( heatSource_1, 'heatSource_1' )
geompy.addToStudy( Fuse_2, 'Fuse_2' )
geompy.addToStudy( Compound_1, 'Compound_1' )
geompy.addToStudy( Partition_1, 'Partition_1' )
geompy.addToStudyInFather( Partition_1, heatSourceSolid, 'heatSourceSolid' )
geompy.addToStudyInFather( Partition_1, plateSolid, 'plateSolid' )
geompy.addToStudyInFather( Partition_1, BoxOuterFaces, 'BoxOuterFaces' )
geompy.addToStudyInFather( Partition_1, PlateUpperFace, 'PlateUpperFace' )
geompy.addToStudyInFather( Fuse_2, FixedLine, 'FixedLine' )
geompy.addToStudyInFather( Fuse_2, inletSurface, 'inletSurface' )
geompy.addToStudyInFather( Partition_1, AllFaces, 'AllFaces' )
geompy.addToStudyInFather( Partition_1, HeatFluxFaces, 'HeatFluxFaces' )
geompy.addToStudyInFather( Partition_1, ZeroFluxFaces0, 'ZeroFluxFaces0' )
geompy.addToStudyInFather( Partition_1, BoxPlateInterface, 'BoxPlateInterface' )
geompy.addToStudyInFather( Partition_1, ZeroFluxFaces, 'ZeroFluxFaces' )
FixedLine = FixedLine
inletSurface = inletSurface

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
  Mesh_1.ExportUNV( r'meshTest.unv' )
except:
  print 'ExportUNV() failed. Invalid file name?'
Mesh_2 = smesh.Mesh(Partition_1)
status = Mesh_2.AddHypothesis(MaxLength_0_0004)
Regular_1D_1 = Mesh_2.Segment()
MEFISTO_2D_1 = Mesh_2.Triangle(algo=smeshBuilder.MEFISTO)
NETGEN_3D_1 = Mesh_2.Tetrahedron()
isDone = Mesh_2.Compute()
heatSourceSolid_1 = Mesh_2.GroupOnGeom(heatSourceSolid,'heatSourceSolid',SMESH.VOLUME)
plateSolid_1 = Mesh_2.GroupOnGeom(plateSolid,'plateSolid',SMESH.VOLUME)
BoxOuterFaces_1 = Mesh_2.GroupOnGeom(BoxOuterFaces,'BoxOuterFaces',SMESH.FACE)
PlateUpperFace_1 = Mesh_2.GroupOnGeom(PlateUpperFace,'PlateUpperFace',SMESH.FACE)
FixedLine_3 = Mesh_2.GroupOnGeom(FixedLine,'FixedLine',SMESH.EDGE)
inletSurface_3 = Mesh_2.GroupOnGeom(inletSurface,'inletSurface',SMESH.FACE)
HeatFluxFaces_1 = Mesh_2.GroupOnGeom(HeatFluxFaces,'HeatFluxFaces',SMESH.FACE)
ZeroFluxFaces_1 = Mesh_2.GroupOnGeom(ZeroFluxFaces,'ZeroFluxFaces',SMESH.FACE)
heatSourceSolid_2 = Mesh_2.GroupOnGeom(heatSourceSolid,'heatSourceSolid',SMESH.NODE)
plateSolid_2 = Mesh_2.GroupOnGeom(plateSolid,'plateSolid',SMESH.NODE)
BoxOuterFaces_2 = Mesh_2.GroupOnGeom(BoxOuterFaces,'BoxOuterFaces',SMESH.NODE)
PlateUpperFace_2 = Mesh_2.GroupOnGeom(PlateUpperFace,'PlateUpperFace',SMESH.NODE)
FixedLine_4 = Mesh_2.GroupOnGeom(FixedLine,'FixedLine',SMESH.NODE)
inletSurface_4 = Mesh_2.GroupOnGeom(inletSurface,'inletSurface',SMESH.NODE)
HeatFluxFaces_2 = Mesh_2.GroupOnGeom(HeatFluxFaces,'HeatFluxFaces',SMESH.NODE)
ZeroFluxFaces_2 = Mesh_2.GroupOnGeom(ZeroFluxFaces,'ZeroFluxFaces',SMESH.NODE)
try:
  Mesh_2.ExportUNV( r'/home/marmar/scratch/parallelWorks/heatTransfer/workflow_DEX_fixedPoints/models/mesh/Mesh_2.unv' )
except:
  print 'ExportUNV() failed. Invalid file name?'


## Set names of Mesh objects
smesh.SetName(FixedLine_3, 'FixedLine')
smesh.SetName(ZeroFluxFaces_2, 'ZeroFluxFaces')
smesh.SetName(FixedLine_4, 'FixedLine')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(PlateUpperFace_2, 'PlateUpperFace')
smesh.SetName(HeatFluxFaces_2, 'HeatFluxFaces')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
smesh.SetName(inletSurface_4, 'inletSurface')
smesh.SetName(MEFISTO_2D.GetAlgorithm(), 'MEFISTO_2D')
smesh.SetName(heatSourceSolid_2, 'heatSourceSolid')
smesh.SetName(BoxOuterFaces_2, 'BoxOuterFaces')
smesh.SetName(heatSourceSolid_1, 'heatSourceSolid')
smesh.SetName(plateSolid_2, 'plateSolid')
smesh.SetName(plateSolid_1, 'plateSolid')
smesh.SetName(MaxLength_0_0004, 'MaxLength=0.0004')
smesh.SetName(inletSurface_1, 'inletSurface')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Mesh_2.GetMesh(), 'Mesh_2')
smesh.SetName(ZeroFluxFaces_1, 'ZeroFluxFaces')
smesh.SetName(HeatFluxFaces_1, 'HeatFluxFaces')
smesh.SetName(inletSurface_3, 'inletSurface')
smesh.SetName(PlateUpperFace_1, 'PlateUpperFace')
smesh.SetName(FixedLine_1, 'FixedLine')
smesh.SetName(BoxOuterFaces_1, 'BoxOuterFaces')
smesh.SetName(inletSurface_2, 'inletSurface')
smesh.SetName(FixedLine_2, 'FixedLine')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
