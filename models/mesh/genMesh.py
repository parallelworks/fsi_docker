# -*- coding: utf-8 -*-

import sys,os
import salome

salome.salome_init()
theStudy = salome.myStudy

inputFileName = sys.argv[1]

if len(sys.argv) > 2:
    meshFileName = sys.argv[2]
else:
    meshFileName = "mesh.unv"

import data_IO

in_fp = data_IO.open_file(inputFileName)

# geom parameters
Length = data_IO.read_float_from_file_pointer(in_fp, "Length")
Width = data_IO.read_float_from_file_pointer(in_fp, "Width")
Height = data_IO.read_float_from_file_pointer(in_fp, "Height")
Thickness = data_IO.read_float_from_file_pointer(in_fp, "Thickness")
InletLength = data_IO.read_float_from_file_pointer(in_fp, "InletLength")
OutletLength = data_IO.read_float_from_file_pointer(in_fp, "OutletLength")
InletHeight = data_IO.read_float_from_file_pointer(in_fp, "InletHeight")
OutletHeight = data_IO.read_float_from_file_pointer(in_fp, "OutletHeight")
InletOffset = data_IO.read_float_from_file_pointer(in_fp, "InletOffset")
OutletOffset = data_IO.read_float_from_file_pointer(in_fp, "OutletOffset")
HeatSource_LX = 0.002 
HeatSource_LY = 0.003
HeatSource_LZ = 0.001
HeatSource_X = 0.002 
HeatSource_Y = -0.001
plate_LX = 0.008
plate_LY = 0.01
plate_LZ = 0.0005
plate_X = 0.0
plate_Y = 0.0


# mesh parameters
meshRes = data_IO.read_float_from_file_pointer(in_fp, "meshRes")

"""
Length=0.01
Width=0.01
Height=0.0025
Thickness=0.00025
InOutLength=0.001
meshRes=0.0005
"""

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
Box_1 = geompy.MakeBoxDXDYDZ(Length, Width, Height)
Translation_1 = geompy.MakeTranslation(Box_1, -Length/2, -Width/2, 0)

# box
[Face_1,Face_2,Face_3,Face_4,Face_5,Face_6] = geompy.ExtractShapes(Translation_1, geompy.ShapeType["FACE"], True)
Extrusion_1 = geompy.MakePrismVecH(Face_1, OX, Thickness)
Extrusion_2 = geompy.MakePrismVecH(Face_2, OY, Thickness)
Extrusion_3 = geompy.MakePrismVecH(Face_5, OY, -Thickness)
Extrusion_4 = geompy.MakePrismVecH(Face_6, OX, -Thickness)
Extrusion_5 = geompy.MakePrismVecH(Face_4, OZ, -Thickness)
Extrusion_6 = geompy.MakePrismVecH(Face_3, OZ, Thickness)
Fuse_1 = geompy.MakeFuseList([Extrusion_1, Extrusion_2, Extrusion_3, Extrusion_4, Extrusion_5, Extrusion_6], True, True)

# inlet
Circle_1 = geompy.MakeCircle(O, OY, ((Height-(2*Thickness))/2)*InletHeight)
Circle_2 = geompy.MakeCircle(O, OY, ((Height-(2*Thickness))/2)*InletHeight-Thickness*InletHeight)
Face_7 = geompy.MakeFaceWires([Circle_1, Circle_2], 1)
Translation_2 = geompy.MakeTranslation(Face_7, 0, (Width/2)-Thickness, Height/2)
Extrusion_7 = geompy.MakePrismVecH(Translation_2, OY, InletLength+Thickness)
Extrusion_7a = geompy.MakeTranslation(Extrusion_7, (Length/2-((Height-(2*Thickness))/2)-Thickness)*InletOffset , 0, 0)

# outlet
Circle_3 = geompy.MakeCircle(O, OY, ((Height-(2*Thickness))/2)*OutletHeight)
Circle_4 = geompy.MakeCircle(O, OY, ((Height-(2*Thickness))/2)*OutletHeight-Thickness*OutletHeight)
Face_8 = geompy.MakeFaceWires([Circle_3, Circle_4], 1)
Translation_22 = geompy.MakeTranslation(Face_8, 0, -((Width/2)-Thickness), Height/2)
Extrusion_8 = geompy.MakePrismVecH(Translation_22, OY, -(OutletLength+Thickness))
Extrusion_8a = geompy.MakeTranslation(Extrusion_8, (Length/2-((Height-(2*Thickness))/2)-Thickness)*OutletOffset , 0, 0)

Cut_1 = geompy.MakeCutList(Fuse_1, [Extrusion_7a, Extrusion_8a], True)
[Solid_1,Solid_2,Solid_3] = geompy.ExtractShapes(Cut_1, geompy.ShapeType["SOLID"], True)

# Add a block for a heat source

plate = geompy.MakeBoxDXDYDZ(plate_LX, plate_LY, plate_LZ)
plate_1 = geompy.MakeTranslation(plate, -plate_LX/2.0 + plate_X, -plate_LY/2.0 + plate_Y, Thickness)

heatSource = geompy.MakeBoxDXDYDZ(HeatSource_LX, HeatSource_LY, HeatSource_LZ)
heatSource_1 = geompy.MakeTranslation(heatSource, -HeatSource_LX/2.0 + HeatSource_X, -HeatSource_LY/2.0 + HeatSource_Y, Thickness + plate_LZ)

Fuse_2 = geompy.MakeFuseList([Extrusion_7a, Extrusion_8a, Solid_2], True, True)

[Face_1,Face_2,InFace] = geompy.ExtractShapes(Solid_1, geompy.ShapeType["FACE"], True)
[OutFace,Face_5,Face_6] = geompy.ExtractShapes(Solid_3, geompy.ShapeType["FACE"], True)

Inlet = geompy.MakeTranslation(InFace, 0, InletLength, 0)
Outlet = geompy.MakeTranslation(OutFace, 0, -OutletLength, 0)


Compound_1 = geompy.MakeCompound([heatSource_1, plate_1, Fuse_2])
Partition_1 = geompy.MakePartition([Compound_1], [], [], [], geompy.ShapeType["SOLID"], 0, [], 1)

# listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["VERTEX"])
# listSubShapeIDs = geompy.SubShapeAllIDs(Fuse_2, geompy.ShapeType["EDGE"])
# FixedLine = geompy.CreateGroup(Fuse_2, geompy.ShapeType["EDGE"])
# geompy.UnionIDs(FixedLine, [32, 17])
# inletSurface = geompy.CreateGroup(Fuse_2, geompy.ShapeType["FACE"])
# geompy.UnionIDs(inletSurface, [66])

listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["SOLID"])
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["EDGE"])

heatSourceSolid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(heatSourceSolid, [2])

[geomObj_37,geomObj_38,geomObj_39,geomObj_40,geomObj_41,geomObj_42] = geompy.SubShapeAll(heatSourceSolid, geompy.ShapeType["FACE"])
[geomObj_43,geomObj_44,geomObj_45,geomObj_46,geomObj_47,geomObj_48] = geompy.SubShapeAll(heatSourceSolid, geompy.ShapeType["FACE"])

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

listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_37)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_38)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_39)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_40)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_41)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_42)

BoxPlateInterface = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(BoxPlateInterface, [26])

listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_43)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_44)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_45)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_46)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_47)
listSameIDs = geompy.GetSameIDs(Partition_1, geomObj_48)
ZeroFluxFaces = geompy.CutListOfGroups([ZeroFluxFaces0], [BoxPlateInterface])



geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Extrusion_7a, 'Extrusion_7a')
geompy.addToStudy( Extrusion_8a, 'Extrusion_8a')
geompy.addToStudy( Solid_2, 'Solid_2' )
geompy.addToStudy( heatSource, 'heatSource' )
geompy.addToStudy( heatSource_1, 'heatSource_1' )
geompy.addToStudy( plate, 'plate' )
geompy.addToStudy( plate_1, 'plate_1' )
geompy.addToStudy( Fuse_2, 'Fuse_2' )
geompy.addToStudyInFather( Fuse_2, FixedLine, 'FixedLine' )
geompy.addToStudyInFather( Fuse_2, inletSurface, 'inletSurface' )
geompy.addToStudy( Compound_1, 'Compound_1' )
geompy.addToStudy( Partition_1, 'Partition_1' )

geompy.addToStudyInFather( Fuse_2, FixedLine, 'FixedLine' )
geompy.addToStudyInFather( Fuse_2, inletSurface, 'inletSurface' )
geompy.addToStudyInFather( Partition_1, heatSourceSolid, 'heatSourceSolid' )
geompy.addToStudyInFather( Partition_1, plateSolid, 'plateSolid' )
geompy.addToStudyInFather( Partition_1, BoxOuterFaces, 'BoxOuterFaces' )
geompy.addToStudyInFather( Partition_1, PlateUpperFace, 'PlateUpperFace' )
geompy.addToStudyInFather( Partition_1, FixedLine, 'FixedLine' )
geompy.addToStudyInFather( Partition_1, inletSurface, 'inletSurface' )
geompy.addToStudyInFather( Partition_1, AllFaces, 'AllFaces' )
geompy.addToStudyInFather( Partition_1, HeatFluxFaces, 'HeatFluxFaces' )
geompy.addToStudyInFather( Partition_1, ZeroFluxFaces0, 'ZeroFluxFaces0' )
geompy.addToStudyInFather( Partition_1, BoxPlateInterface, 'BoxPlateInterface' )
geompy.addToStudyInFather( Partition_1, ZeroFluxFaces, 'ZeroFluxFaces' )


#geompy.ExportSTL(Fuse_2, meshFileName.replace("mesh.unv","body.stl"), False )
geompy.ExportSTL(Partition_1, "body.stl", True, 0.001, True)
geompy.ExportSTL(Inlet, meshFileName.replace("mesh.unv","inlet.stl"), False )
geompy.ExportSTL(Outlet, meshFileName.replace("mesh.unv","outlet.stl"), False )
geompy.ExportSTL(ZeroFluxFaces, "ZeroFluxFaces.stl", True, 0.001, True)
geompy.ExportSTL(HeatFluxFaces, "HeatFluxFaces.stl", True, 0.001, True)


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
# Mesh_1 = smesh.Mesh(Fuse_2)
Mesh_1 = smesh.Mesh(Partition_1)
Regular_1D = Mesh_1.Segment()
Max_Size_1 = Regular_1D.MaxSize(meshRes)
MEFISTO_2D = Mesh_1.Triangle(algo=smeshBuilder.MEFISTO)
NETGEN_3D = Mesh_1.Tetrahedron()

isDone = Mesh_1.Compute()

# FixedLine_1 = Mesh_1.GroupOnGeom(FixedLine,'FixedLine',SMESH.EDGE)
# inletSurface_1 = Mesh_1.GroupOnGeom(inletSurface,'inletSurface',SMESH.FACE)
# FixedLine_2 = Mesh_1.GroupOnGeom(FixedLine,'FixedLine',SMESH.NODE)
# inletSurface_2 = Mesh_1.GroupOnGeom(inletSurface,'inletSurface',SMESH.NODE)

heatSourceSolid_1 = Mesh_1.GroupOnGeom(heatSourceSolid,'heatSourceSolid',SMESH.VOLUME)
plateSolid_1 = Mesh_1.GroupOnGeom(plateSolid,'plateSolid',SMESH.VOLUME)
BoxOuterFaces_1 = Mesh_1.GroupOnGeom(BoxOuterFaces,'BoxOuterFaces',SMESH.FACE)
PlateUpperFace_1 = Mesh_1.GroupOnGeom(PlateUpperFace,'PlateUpperFace',SMESH.FACE)
FixedLine_1 = Mesh_1.GroupOnGeom(FixedLine,'FixedLine',SMESH.EDGE)
inletSurface_1 = Mesh_1.GroupOnGeom(inletSurface,'inletSurface',SMESH.FACE)
HeatFluxFaces_1 = Mesh_1.GroupOnGeom(HeatFluxFaces,'HeatFluxFaces',SMESH.FACE)
ZeroFluxFaces_1 = Mesh_1.GroupOnGeom(ZeroFluxFaces,'ZeroFluxFaces',SMESH.FACE)
heatSourceSolid_2 = Mesh_1.GroupOnGeom(heatSourceSolid,'heatSourceSolid',SMESH.NODE)
plateSolid_2 = Mesh_1.GroupOnGeom(plateSolid,'plateSolid',SMESH.NODE)
BoxOuterFaces_2 = Mesh_1.GroupOnGeom(BoxOuterFaces,'BoxOuterFaces',SMESH.NODE)
PlateUpperFace_2 = Mesh_1.GroupOnGeom(PlateUpperFace,'PlateUpperFace',SMESH.NODE)
FixedLine_2 = Mesh_1.GroupOnGeom(FixedLine,'FixedLine',SMESH.NODE)
inletSurface_2 = Mesh_1.GroupOnGeom(inletSurface,'inletSurface',SMESH.NODE)
HeatFluxFaces_2 = Mesh_1.GroupOnGeom(HeatFluxFaces,'HeatFluxFaces',SMESH.NODE)
ZeroFluxFaces_2 = Mesh_1.GroupOnGeom(ZeroFluxFaces,'ZeroFluxFaces',SMESH.NODE)

## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
smesh.SetName(MEFISTO_2D.GetAlgorithm(), 'MEFISTO_2D')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')

## Set names of Mesh objects
smesh.SetName(heatSourceSolid_1, 'heatSourceSolid')
smesh.SetName(heatSourceSolid_2, 'heatSourceSolid')

smesh.SetName(plateSolid_1, 'plateSolid')
smesh.SetName(plateSolid_2, 'plateSolid')

smesh.SetName(BoxOuterFaces_1, 'BoxOuterFaces')
smesh.SetName(BoxOuterFaces_2, 'BoxOuterFaces')

smesh.SetName(PlateUpperFace_1, 'PlateUpperFace')
smesh.SetName(PlateUpperFace_2, 'PlateUpperFace')

smesh.SetName(FixedLine_1, 'FixedLine')
smesh.SetName(FixedLine_2, 'FixedLine')

smesh.SetName(inletSurface_1, 'inletSurface')
smesh.SetName(inletSurface_2, 'inletSurface')

smesh.SetName(HeatFluxFaces_1, 'HeatFluxFaces')
smesh.SetName(HeatFluxFaces_2, 'HeatFluxFaces')

smesh.SetName(ZeroFluxFaces_1, 'ZeroFluxFaces')
smesh.SetName(ZeroFluxFaces_2, 'ZeroFluxFaces')

Mesh_1.ExportUNV( meshFileName )
#Mesh_1.ExportSTL(meshFileName.replace("mesh.unv","mesh.stl"), True )
