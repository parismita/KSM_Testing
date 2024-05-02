import pandas as pd
import os

# Directory containing the CSV files
directory = 'results'

# Create a list to hold data from each CSV file
dataframes = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Create the complete filepath
        filepath = os.path.join(directory, filename)
        parts = filename.replace('.csv', '').split('_')
        df = pd.read_csv(filepath)
        means = df.mean()
        means_series = pd.Series(means)
        means_df = pd.DataFrame(means_series).transpose()
        means_df = means_df.iloc[:, 1:]
        means_df.to_csv('means.csv')
        means_df['scan_rate'] = int((df["FullScans"].max()-df["FullScans"].min())/len(df))
        means_df['num_process'] = int(parts[1])
        means_df['dirty_time'] = parts[2]
        means_df['num_pages_to_scan'] = int(parts[3])
        means_df['sleep_millis'] = int(parts[4])
        dataframes.append(means_df)
        

combined_csv = pd.concat(dataframes, ignore_index=True)
combined_csv.to_csv('combined_file.csv', index=False)