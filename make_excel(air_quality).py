# import re
# import pandas as pd

# # Read data from the text file
# with open("data.txt", "r") as file:
#     data = file.read()

# # Use regular expressions to extract relevant data
# timestamp_matches = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})', data)
# humidity_matches = re.findall(r'Humidity: (.*?)\s+', data)
# temperature_matches = re.findall(r'Temperature: (.*?)\s+', data)
# mq135_data_matches = re.findall(r'MQ135 RZero: (.*?)\s+Corrected RZero: (.*?)\s+Resistance: (.*?)\s+PPM: (.*?)\s+Corrected PPM: (.*?)ppm', data)

# # Create a list of dictionaries with the extracted values
# data_list = []

# for timestamp, humidity, temperature, mq135_data in zip(timestamp_matches, humidity_matches, temperature_matches, mq135_data_matches):
#     data_dict = {
#         'Time': [timestamp],
#         'Humidity': [humidity],
#         'Temperature': [temperature],
#         'MQ135 RZero': [mq135_data[0]],
#         'Corrected RZero': [mq135_data[1]],
#         'Resistance': [mq135_data[2]],
#         'PPM': [mq135_data[3]],
#         'Corrected PPM': [mq135_data[4]]
#     }
#     data_list.append(data_dict)

# # Create a Pandas DataFrame from the list of dictionaries
# df = pd.concat([pd.DataFrame(data_dict) for data_dict in data_list], ignore_index=True)

# # Create an Excel writer object
# excel_writer = pd.ExcelWriter('formatted_data.xlsx', engine='openpyxl')

# # Write the DataFrame to an Excel sheet with the specified column order
# df[['Time', 'Humidity', 'Temperature', 'MQ135 RZero', 'Corrected RZero', 'Resistance', 'PPM', 'Corrected PPM']].to_excel(excel_writer, sheet_name='Data', index=False)

# # Save the Excel file
# excel_writer.close()

# print("Data has been saved to formatted_data.xlsx")
import re
import pandas as pd
import tkinter.filedialog
import os
data_file = tkinter.filedialog.askopenfilename()
# Read data from the text file
with open(data_file, "r") as file:
    data = file.read()

# Use regular expressions to extract relevant data
timestamp_matches = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})', data)
humidity_matches = re.findall(r'Humidity: (.*?)\s+', data)
temperature_matches = re.findall(r'Temperature: (.*?)\s+', data)
mq135_data_matches = re.findall(r'MQ135 RZero: (.*?)\s+Corrected RZero: (.*?)\s+Resistance: (.*?)\s+PPM: (.*?)\s+Corrected PPM: (.*?)ppm', data)

# Create a list of dictionaries with the extracted values
data_list = []

for timestamp, humidity, temperature, mq135_data in zip(timestamp_matches, humidity_matches, temperature_matches, mq135_data_matches):
    data_dict = {
        'Time': [timestamp],
        'Humidity': [humidity],
        'Temperature': [temperature],
        'MQ135 RZero': [mq135_data[0]],
        'Corrected RZero': [mq135_data[1]],
        'Resistance': [mq135_data[2]],
    }
    data_list.append(data_dict)

# Create a Pandas DataFrame from the list of dictionaries
df = pd.concat([pd.DataFrame(data_dict) for data_dict in data_list], ignore_index=True)

# Create an Excel writer object
excel_writer = pd.ExcelWriter(f'formatted_{os.path.split(data_file)[1]}.xlsx', engine='openpyxl')

# Write the DataFrame to an Excel sheet with the specified column order
df[['Time', 'Humidity', 'Temperature', 'MQ135 RZero', 'Corrected RZero', 'Resistance']].to_excel(excel_writer, sheet_name='Data', index=False)

# Save the Excel file
excel_writer.close()

print("Data has been saved to formatted_data.xlsx")
