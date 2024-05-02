#!/bin/bash

if [ $# -ne 8 ]; then
    echo "Usage: $0 <num_process> <num_pages_per_process> <number_of_rounds> <round_wait_time> <pages_to_scan> <sleep_millisecs> <test_time> <outputfilename>"
    exit 1
fi

sudo systemctl stop ksmtuned.service
sudo systemctl disable ksmtuned.service
sudo systemctl restart ksm.service 

# make executable
./build.sh

# Usage: ./spawner.sh <num_process> <num_pages_per_process> <number_of_rounds> <round_wait_time>
./spawner_process.sh $1 $2 $3 $4 # change this parameter

# start monitoring 
set_ksm_parameters() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        echo "Error: File '$file' not found."
        return 1
    fi

    # Read the file line by line and set KSM parameters
    while IFS='=' read -r key value; do
        case $key in
            max_page_sharing)
                echo "$value" > /sys/kernel/mm/ksm/max_page_sharing
                ;;
            merge_across_nodes)
                echo "$value" > /sys/kernel/mm/ksm/merge_across_nodes
                ;;
            pages_to_scan)
                echo "$value" > /sys/kernel/mm/ksm/pages_to_scan
                ;;
            run)
                echo "$value" > /sys/kernel/mm/ksm/run
                ;;
            sleep_millisecs)
                echo "$value" > /sys/kernel/mm/ksm/sleep_millisecs
                ;;
            stable_node_chains_prune_millisecs)
                echo "$value" > /sys/kernel/mm/ksm/stable_node_chains_prune_millisecs
                ;;
            use_zero_pages)
                echo "$value" > /sys/kernel/mm/ksm/use_zero_pages
                ;;
            *)
                echo "Unknown parameter: $key"
                ;;
        esac
    done < "$file"

    echo "KSM parameters set based on $file"
}


handle_sigint() {
    echo "Ctrl+C pressed, exiting..."
    echo "Ending Test"
    set_ksm_parameters defualt_ksm_config
    pkill -9 process
    exit 0
}

trap 'handle_sigint' SIGINT


echo "1" > /sys/kernel/mm/ksm/run
echo "$5" > /sys/kernel/mm/ksm/pages_to_scan
echo "$6" > /sys/kernel/mm/ksm/sleep_millisecs
test_time=$7


cat /sys/kernel/mm/ksm/pages_to_scan
cat /sys/kernel/mm/ksm/sleep_millisecs
cat /sys/kernel/mm/ksm/run
rm -rf $8
printf "| %-9s| %-13s| %-16s| %-16s| %-15s| %-15s| %-15s|\n" "FullScans" "GeneralProfit" "PagesShared" "TotalPagesShared" "PagesNotShared" "PagesVolatile" "KSM_CPU"
echo "FullScans,GeneralProfit,PagesShared,TotalPagesShared,PagesNotShared,PagesVolatile,KSM_CPU" >> $8

while [ $test_time -ne 0 ]; do
    full_scans=$(cat /sys/kernel/mm/ksm/full_scans)
    general_profit=$(cat /sys/kernel/mm/ksm/general_profit)
    total_pages_shared=$(cat /sys/kernel/mm/ksm/pages_shared)
    pages_currently_shared=$(cat /sys/kernel/mm/ksm/pages_sharing)
    pages_to_scan=$(cat /sys/kernel/mm/ksm/pages_to_scan)
    pages_nolonger_shared=$(cat /sys/kernel/mm/ksm/pages_unshared)
    pages_volatile=$(cat /sys/kernel/mm/ksm/pages_volatile)
    # ksm_cpu=$(top -n 1 -p 47 -o %CPU | grep ksmd | awk '{print $10}')
    ksm_cpu=$(pidstat -u -p 47 1 1 | grep "Average" | awk '{print $8}')
    printf "| %-9s| %-13s| %-16s| %-16s| %-15s| %-15s| %-15s|\n" "$full_scans" "$general_profit" "$total_pages_shared" "$pages_currently_shared" "$pages_nolonger_shared" "$pages_volatile" "$ksm_cpu" 
    echo "$full_scans,$general_profit,$total_pages_shared,$pages_currently_shared,$pages_nolonger_shared,$pages_volatile,$ksm_cpu" >> $8    
    # sleep 1 
    ((test_time--))
done

echo "Ending Test"
set_ksm_parameters defualt_ksm_config

pids=$(pgrep -x process)

if [ -n "$pids" ]; then
    for pid in $pids; do
        kill -9 "$pid"
    done
else
    echo "No processes found with the name 'process'."
fi