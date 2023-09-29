
import customtkinter as ctk
import threading
import time
import serial

from tkinter import filedialog

# Initialize variables to store user inputs
selected_port = ""
output_file_name = ""
output_path = ""
baud_rate_val = ""
# Create a flag to control the data gathering thread
data_gathering = False

# Function to gather data in a separate thread
def gather_data_thread():
    global selected_port
    global selected_baud_rate
    global output_file_name
    global output_path
    global baud_rate_val

    with open(output_path + "/" + output_file_name, 'w') as file:
        time.sleep(0.5)

        ser = serial.Serial(selected_port, baud_rate_val, timeout=1.5)
        while data_gathering:
            data = ser.readline().decode().strip()
            file.write(data + '\n')
            file.flush()
            print(data)

# Function to start/stop data gathering
def toggle_data_gathering():
    global data_gathering
    global selected_port
    global baud_rate_val
    global output_file_name
    global output_path

    global ard_port  # Added to access the ComboBox

    if data_gathering:
        data_gathering = False
        toggle_button.configure(text="Start gathering")
    else:
        data_gathering = True
        toggle_button.configure(text="Stop gathering")

        # Get the selected port from the ComboBox
        selected_port = ard_port.get()

        # Get the output file name and path from the Entry widgets
        output_file_name = file_name.get()

        # Open a file dialog to select the output path
        output_path = save_path.get()
        baud_rate_val = baud_rate.get()
        # Start the data gathering thread
        data_thread = threading.Thread(target=gather_data_thread)
        data_thread.start()

def on_baud_rate_select(event):
    global selected_baud_rate
    selected_baud_rate = baud_rate.get()

root = ctk.CTk()
root.geometry("750x200")
root.title("Data Gather")
root.resizable(False, False)

ard_port_label = ctk.CTkLabel(root, text="Arduino Port")
ard_port_label.grid(row=0, column=0, padx=3)

ard_port = ctk.CTkComboBox(root, values=["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9"])
ard_port.grid(row=0, column=1, pady=10, padx=10, sticky="w")

ard_port_label = ctk.CTkLabel(root, text="Arduino Port")
ard_port_label.grid(row=0, column=0, padx=3)

baud_rate_label = ctk.CTkLabel(root, text="Baud Rate")
baud_rate_label.grid(row=0, column=1, columnspan=1, sticky="e")

baud_rate = ctk.CTkComboBox(root, values=["9600", "115200", "57600", "38400", "19200", "14400", "1200", "300"])
baud_rate.grid(row=0, column=2, pady=10, padx=20)
baud_rate.set("9600")
  # Bind the event handler

file_label = ctk.CTkLabel(root, text="Name for the output file")
file_label.grid(row=1, padx=15)
file_name = ctk.CTkEntry(root, width=300, height=10)
file_name.grid(row=1, column=1, columnspan=1, pady=10, padx=10)

save_path_label = ctk.CTkLabel(root, text="Path where to save the output file")
save_path_label.grid(row=2, column=0, padx=10)

save_path = ctk.CTkEntry(root, width=300, height=10)
save_path.grid(row=2, column=1, padx=10)

# Add a "Browse" button to select the output path
def browse_path():
    global output_path
    output_path = filedialog.askdirectory()  # Open a folder selection dialog
    save_path.delete(0, 'end')  # Clear the existing text in the Entry widget
    save_path.insert(0, output_path)  # Update the Entry widget with the selected path

browse_button = ctk.CTkButton(root, text="Browse", command=browse_path, width=30, height=20)
browse_button.grid(row=2, column=2)

toggle_button = ctk.CTkButton(root, command=toggle_data_gathering, text="Start gathering", width=55, height=35)
toggle_button.grid(row=3, column=0, columnspan=3, pady=10)

print("Selected Port:", selected_port)
print("Output File Name:", output_file_name)
print("Output Path:", output_path)
print("Selected Baud Rate:", baud_rate_val)
root.mainloop()

# After the Tkinter main loop exits, you can access the values:
print("Selected Port:", selected_port)
print("Output File Name:", output_file_name)
print("Output Path:", output_path)
print("Selected Baud Rate:", baud_rate_val)