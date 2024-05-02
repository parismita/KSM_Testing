import os
import pandas as pd
import matplotlib.pyplot as plt
import re


num_of_process_range = range(1, 6, 1)
round_time_range = range(1, 4, 1)
pages_to_scan_range = range(500, 2501, 500)
sleep_millisecs_range = [1, 5, 10, 15]

# Constants
output_dir = "results"
pages_to_scan_range = [500, 2000, 3500, 5000]
sleep_millisecs_range = [3, 12, 21, 30]
round_time_range=[1,3,5,7,9]
const_pages_to_scan=1500
const_sleep_millisec=21
const_round_time=5


plots_dir = "test_plots"
os.makedirs(plots_dir, exist_ok=True)


def find_matching_filename(param_value, param_type):
    """Finds a filename that matches the given parameter value."""
    if param_type == "Pages to Scan":
        pattern = re.compile(rf"dat_{param_value}_{const_sleep_millisec}_{const_round_time}\.csv")
    elif param_type == "Sleep Millisecs":
        pattern = re.compile(rf"dat_{const_pages_to_scan}_{param_value}_{const_round_time}\.csv")
    elif param_type == "Round Time":
        pattern = re.compile(rf"dat_{const_pages_to_scan}_{const_sleep_millisec}_{param_value}\.csv")
    
    for filename in os.listdir(output_dir):
        if pattern.search(filename):
            return os.path.join(output_dir, filename)
    return None

def plot_param(column_name, param_range, param_type):
    """Plots graphs for each column from multiple files with different parameter values."""
    plt.figure(figsize=(10, 6))

    for param in param_range:
        file_path = find_matching_filename(param, param_type)
        if file_path:
            data = pd.read_csv(file_path)
            plt.plot(data['Time'], data[column_name], label=f'{param_type}={param}')
        else:
            print(f"No file found for {param_type}={param}")

    plt.title(f"Comparison of {column_name} VS Time for Different {param_type}")
    plt.xlabel("Time (seconds)")
    plt.ylabel(column_name)
    plt.legend()
    plt.savefig(f"{plots_dir}/plot_{column_name}_{param_type}.png")
    plt.close()

def plot_cpu_util(param_range, param_type):
    """Plots graphs for cpu util from multiple files with different parameter values."""
    plt.figure(figsize=(10, 6))
    max_cpu_util = []
    column_name = "CPU_Utilization"
    for param in param_range:
        file_path = find_matching_filename(param, param_type)
        if file_path:
            data = pd.read_csv(file_path)
            max_cpu_util += [data.columns[6].max()]
        else:
            print(f"No file found for {param_type}={param}")

    plt.title(f"Comparison of {column_name} VS {param_type}")
    plt.bar(param_range, max_cpu_util, color='red')
    plt.xlabel(f"{param_type}")
    plt.ylabel(column_name)
    plt.legend()
    plt.savefig(f"{plots_dir}/plot_max_{column_name}_{param_type}.png")
    plt.close()


if __name__ == "__main__":
    # Assuming the first file contains all necessary columns
    example_file = find_matching_filename(1000, "Pages to Scan")


    data = pd.read_csv(example_file)
    for column_name in data.columns:  # Skip 'Time' column
        plot_param(column_name, pages_to_scan_range, "Pages to Scan")
        plot_param(column_name, sleep_millisecs_range, "Sleep Millisecs")
        plot_param(column_name, round_time_range, "Round Time")


    plot_cpu_util(range(500 5001, 500), "Pages to Scan")
    plot_cpu_util(range(3, 31, 3), "Sleep Millisecs")
    plot_cpu_util(range(1, 5, 1), "Round Time")

