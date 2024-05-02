#!/bin/bash

# This script is used to spawn multiple writer process on core0 and core1 

if [ $# -ne 4 ]; then
    echo "Usage: $0 <num_process> <num_pages_per_process> <number_of_rounds> <round_wait_time>"
    exit 1
fi

num_process=$1
num_pages_per_process=$2
number_of_rounds=$3
round_wait_time=$4

p=0
while [ $p -lt $num_process ]
do
    # echo "Process Forked"
    taskset -c $(($p%2)) ./process $num_pages_per_process $number_of_rounds $round_wait_time &
    ((p++))
done