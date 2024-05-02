#!/bin/python3

import subprocess
import os

# Test configuration
num_of_pages_per_process = 10000
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)


def run_test(num_process, round_time, pages_to_scan, sleep_millisecs):
    num_of_rounds = 500
    test_time = 30
    filename = f"{output_dir}/dat_{num_process}_{round_time}_{pages_to_scan}_{sleep_millisecs}.csv"
    cmd = f"./monitor_process.sh {num_process} {num_of_pages_per_process} {num_of_rounds} {round_time} {pages_to_scan} {sleep_millisecs} {test_time} {filename}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, check=True)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running test: {e}")
        print(e.stderr.decode())


def main():
    num_of_process_range = [1]
    round_time_range = [1]
    pages_to_scan_range = range(1000,3001,1000)
    sleep_millisecs_range = [1,5,10,15]

    # Clean up old result files
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    for num_process in num_of_process_range:
        for round_time in round_time_range:
            for pages_to_scan in pages_to_scan_range:
                for sleep_millisecs in sleep_millisecs_range:
                    print(f"Running test with NumProcess={num_process}, round_time={round_time}, pages_to_scan={pages_to_scan}, and sleep_millisecs={sleep_millisecs}")
                    run_test(num_process, round_time, pages_to_scan, sleep_millisecs)


if __name__ == '__main__':
    main()
