#!/bin/bash

echo ""
echo "Running CalculiX Analysis..."
echo $@
echo ""

chmod 777 * -R

export HOME=$PWD

params=$1
meshGeometry=$HOME/$2
bcs=$HOME/$3
metricFile=$4
metricImages=$5

mkdir -p $metricImages

cd ${0%/*} || exit 1

caseParams=params.txt
IFS=',' read -a paramcut <<< "$params"
for (( c=0; c<=$(echo ${#paramcut[@]} - 1 | bc); c=c+2 ))
do
    pname=${paramcut[$c]}
	pval=${paramcut[$c+1]}
	echo $pname $pval >> $caseParams
done

cp $meshGeometry/all.msh ./

tar xzvf $bcs

writeInterval=$(cat $caseParams | grep writeInterval | cut -d " " -f 2)
endTime=$(cat $caseParams | grep endTime | cut -d " " -f 2)

# generate solver input
./writeSolver.sh $writeInterval $endTime

# run ccx
echo ""
echo "Starting CalculiX Run..."
echo ""

# run calculix multi-threaded
NP=2
export OMP_NUM_THREADS=$NP
export CCX_NPROC_RESULTS=$NP
export CCX_NPROC_EQUATION_SOLVER=$NP
export NUMBER_OF_CPUS=$NP

#dir=/opt/calculix
##$dir/cgx-212/cgx_2.12/src/cgx -bg prepmesh.fbd

##$dir/ccx-212-patch/src/ccx_2.12_MT solve -o exo | tee solve.log
#$dir/ccx-212-patch/src/ccx_2.12_MT solve -o exo | tee solve.log | grep --line-buffered total | gawk '{ print strftime("%Y-%m-%d %H:%M:%S"), $0; fflush(); }'

docker run --rm -i -v `pwd`:/scratch -w /scratch -u 0:0 avidalto/calculix:v13 cp /lib/ccx-212-patch.tgz .
tar -xvzf ccx**.tgz
./ccx-212-patch/src/ccx_2.12_MT solve -o exo | tee solve.log | grep --line-buffered total | gawk '{ print strftime("%Y-%m-%d %H:%M:%S"), $0; fflush(); }'

# tail -f -n +1 pipe.log | grep --line-buffered total | gawk '{ print strftime("%Y-%m-%d %H:%M:%S"), $0; fflush(); }'

# extract results
cd $HOME
echo "Extracting CalculiX Results..."
run_command="docker run --rm  -i --user root -v `pwd`:/scratch -w /scratch parallelworks/openfoam:4.1_paraview"
echo $run_command ./models/mexdex/extract.sh /opt/paraview540/bin models/mexdex/extract.py models/calculix/solve.exo models/calculix/kpi.json $metricImages $metricFile
$run_command ./models/mexdex/extract.sh /opt/paraview540/bin models/mexdex/extract.py models/calculix/solve.exo models/calculix/kpi.json $metricImages $metricFile

exit 0
