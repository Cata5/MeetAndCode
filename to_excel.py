import pandas as pd

# Read the CSV data into a DataFrame
try:
    df = pd.read_csv('data.txt')  # Replace 'data.txt' with your file path
    # Save the DataFrame to an Excel file
    df.to_excel('data.xlsx', index=False)
except:
    pass