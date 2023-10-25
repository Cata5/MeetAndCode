import re
import pandas as pd
import tkinter.filedialog
import os

# Ask the user to select the data file using a file dialog
data_file = tkinter.filedialog.askopenfilename()

# Read data from the text file
with open(data_file, "r") as file:
    data = file.read()

# Use regular expressions to extract the timestamp and the entire "Result" field
matches = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}): (\d+)\s+(.*?)$', data, re.MULTILINE)

# Create a list of dictionaries with the extracted values
data_list = []

for timestamp, value, result in matches:
    data_dict = {
        'Time': [timestamp],
        'Value': [value],
        'Result': [result]
    }
    data_list.append(data_dict)

# Create a Pandas DataFrame from the list of dictionaries
df = pd.concat([pd.DataFrame(data_dict) for data_dict in data_list], ignore_index=True)

# Create an Excel writer object
excel_writer = pd.ExcelWriter(f'formatted_{os.path.split(data_file)[1]}.xlsx', engine='openpyxl')

# Write the DataFrame to an Excel sheet with the specified column order
df[['Time', 'Value', 'Result']].to_excel(excel_writer, sheet_name='Data', index=False)

# Save the Excel file
excel_writer.close()

print(f"Data has been saved to formatted_{os.path.split(data_file)[1]}.xlsx")
