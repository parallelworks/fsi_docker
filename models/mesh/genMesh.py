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
Fuse_2 = geompy.MakeFuseList([Extrusion_7a, Extrusion_8a, Solid_2], True, True)

[Face_1,Face_2,InFace] = geompy.ExtractShapes(Solid_1, geompy.ShapeType["FACE"], True)
[OutFace,Face_5,Face_6] = geompy.ExtractShapes(Solid_3, geompy.ShapeType["FACE"], True)

Inlet = geompy.MakeTranslation(InFace, 0, InletLength, 0)
Outlet = geompy.MakeTranslation(OutFace, 0, -OutletLength, 0)

geompy.ExportSTL(Fuse_2, meshFileName.replace("mesh.unv","body.stl"), False )
geompy.ExportSTL(Inlet, meshFileName.replace("mesh.unv","inlet.stl"), False )
geompy.ExportSTL(Outlet, meshFileName.replace("mesh.unv","outlet.stl"), False )


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Fuse_2)
Regular_1D = Mesh_1.Segment()
Max_Size_1 = Regular_1D.MaxSize(meshRes)
MEFISTO_2D = Mesh_1.Triangle(algo=smeshBuilder.MEFISTO)
NETGEN_3D = Mesh_1.Tetrahedron()

isDone = Mesh_1.Compute()
Mesh_1.ExportUNV( meshFileName )
#Mesh_1.ExportSTL(meshFileName.replace("mesh.unv","mesh.stl"), True )
