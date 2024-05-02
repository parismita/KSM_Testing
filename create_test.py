import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os

# Test configuration
num_of_rounds = 30
round_time = 5  # in seconds

num_of_process = 20
num_of_pages_per_process = 100

# Define ranges for test parameters
pages_to_scan_range = range(100, 5000, 100)
sleep_millisecs_range = range(1, 30, 1)

# Fixed configurations for tests
pages_to_scan_configs = [500, 1500, 2500, 3500]  # Example values
sleep_millisecs_configs = [5, 10, 15, 20]  # Example values
fixed_sleep = 20
fixed_pages = 1000

def run_test(test_id, pages_to_scan, sleep_millisecs):
    # Invoke monitor.sh with the specified parameters
    cmd = f"./monitor.sh {num_of_process} {num_of_pages_per_process} {num_of_rounds} {round_time} {pages_to_scan} {sleep_millisecs}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Save output to a CSV file
    filename = f'dat_{test_id}.csv'
    with open(filename, 'w') as f:
        f.write(result.stdout)
    
    return filename

def plot_data(filename, test_id):
    # Load the data from CSV
    data = pd.read_csv(filename)
    columns = data.columns
    
    # Plot each column against time
    for j, column in enumerate(columns, start=1):
        plt.figure()
        plt.plot(data.index, data[column])
        plt.title(f'{column} vs Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel(column)
        graph_filename = f'dat_{test_id}_{j}.png'
        plt.savefig(graph_filename)
        plt.close()

def main():
    test_id = 0
    for pages_to_scan in pages_to_scan_range:
        for sleep_millisecs in sleep_millisecs_range:
            test_id += 1
            print(f"Running test {test_id} with pages_to_scan={pages_to_scan} and sleep_millisecs={sleep_millisecs}")
            csv_filename = run_test(test_id, pages_to_scan, sleep_millisecs)
            

if __name__ == '__main__':
    main()

"""
for qemu-kvm
time vs column 6 graph for pages_to_scan 4, sleep_millisecs 4 total 6+6
amortized cpu util vs pages_to_scan, cpu util vs sleep_millisecs 2

process.c
take these tests for 4 given processes for single pages_to_scan and sleep_millisecs - 14

Total 28 graphs
"""