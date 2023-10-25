import pandas as pd
import matplotlib.pyplot as plt
import tkinter.filedialog 

# Read data from the Excel file
df = pd.read_excel(tkinter.filedialog.askopenfilename())

# Convert the 'Time' column to datetime
df['Time'] = pd.to_datetime(df['Time'])

# Set the 'Time' column as the index (for x-axis in the chart)
df.set_index('Time', inplace=True)

# Create a line chart with multiple lines for each column
df.plot(figsize=(10, 6), title="Sensor Data")
plt.xlabel("Time")
plt.grid(True)

# Customize the chart (if needed)
plt.ylabel("Values")
plt.legend(loc='upper left')

# Show the chart
plt.show()
