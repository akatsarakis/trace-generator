#!/usr/bin/env bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
# Absolute path this script is in, thus /home/user/bin
pushd `dirname $0` > /dev/null
BASEDIR=`pwd`
popd > /dev/null
# set the output path for the traces
tracePath="/home/akatsarakis/Desktop/simulator/traces"
#tracePath="defaultPath"

if [ $tracePath = "defaultPath" ]
then
    tracePath=${BASEDIR}/../traces
    echo $tracePath
fi

# declare parameters to produce traces
declare -a serverNo=(40 80 100)                  #("2" "4" "8" "16" "32" "64" "128")
declare -a writeRatio=(0.00 0.01 0.05 0.10 0.15)       #("0.00" "0.01" "0.05" "0.10" "0.15" "0.50" )
declare -a zipfExp=(0.99)                 #("0.60" "0.70" "0.90" "0.99" "1.01" )
#declare -a workloadSize=("250000000")        #("25000000" "50000000")
declare -a workloadSize=("10000000")        #("25000000" "50000000")
declare -a reqIntervalPerServer=(10)      #("10" "100")
declare -a numberOfKeys=(250000000)       #("125000000" "250000000")
declare -a caseSize=(250000) #in keys     #("250000")

for s in "${serverNo[@]}"  
do 
    for r in "${writeRatio[@]}"
    do
        for a in "${zipfExp[@]}"
        do
            for w in "${workloadSize[@]}"
            do
                for i in "${reqIntervalPerServer[@]}"
                do
                    for k in "${numberOfKeys[@]}"
                    do
                        for c in "${caseSize[@]}"
                        do
                            echo "Running with -s $s -r $r -a $a -w $w -i $i -k $k -c $c"
                            ./../src/runTraceGenerator.py -s $s -r $r -a $a -w $w -i $i -k $k -c $c \
                                > ${tracePath}/trace_w_${w}_k_${k}_c_${c}_s_${s}_r_${r}_a_${a}_i_${i}.txt
                        done
                    done
                done
            done
        done
    done
done
