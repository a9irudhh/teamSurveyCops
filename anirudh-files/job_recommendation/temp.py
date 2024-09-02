import pandas as pd

# Read the CSV files into DataFrames
df1 = pd.read_csv('job_final_1.csv')
df2 = pd.read_csv('job_final_2.csv')

# Concatenate the DataFrames
concatenated_df = pd.concat([df1, df2], ignore_index=True)

# Save the concatenated DataFrame to a new CSV file
concatenated_df.to_csv('job_final_testing.csv', index=False)

print("Files concatenated successfully into 'concatenated_file.csv'.")
