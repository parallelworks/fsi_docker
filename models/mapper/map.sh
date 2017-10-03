#!/bin/bash

echo ""
echo "Running Mapper..."
echo $@
echo ""

chmod 777 * -R

export HOME=$PWD

#body=results/case_0/openfoam/results.tgz
#mesh=results/case_0/mesh/mesh.exo
#results=results/case_0/mapper/results.tgz

body=$HOME/$1
mesh=$HOME/$2
results=$HOME/$3


mkdir -p $(dirname $results)

cp "$body" ${0%/*}
cp "$mesh" ${0%/*} 
cd ${0%/*} || exit 1

tar xzvf results.tgz

mkdir -p bc
ls
docker run --rm  -i -v `pwd`:/scratch -w /scratch -u 0:0 avidalto/python_vtk_pycaster:v1 python map.py body mesh.exo

#cd ${0%/*} || exit 1

tar czvf $results bc

exit 0
