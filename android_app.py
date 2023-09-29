import os
import serial
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock

class DataGatherApp(App):
    def build(self):
        self.selected_port = ""
        self.output_file_name = ""
        self.output_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.baud_rate_val = "9600"
        self.data_gathering = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.ard_port_label = Label(text="Arduino Port:")
        self.ard_port = Spinner(values=["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9"])
        self.baud_rate_label = Label(text="Baud Rate:")
        self.baud_rate = Spinner(values=["9600", "115200", "57600", "38400", "19200", "14400", "1200", "300"],
                                 text=self.baud_rate_val)
        self.baud_rate.bind(on_text_change=self.on_baud_rate_select)
        self.file_label = Label(text="Name for the output file:")
        self.file_name = TextInput()
        self.browse_button = Button(text="Browse")
        self.browse_button.bind(on_press=self.browse_path)
        self.toggle_button = Button(text="Start gathering")
        self.toggle_button.bind(on_press=self.toggle_data_gathering)
        self.log_label = Label(text="")
        self.log_label.height = '100dp'
        self.log_label.text_size = (None, self.log_label.height)
        layout.add_widget(self.ard_port_label)
        layout.add_widget(self.ard_port)
        layout.add_widget(self.baud_rate_label)
        layout.add_widget(self.baud_rate)
        layout.add_widget(self.file_label)
        layout.add_widget(self.file_name)
        layout.add_widget(self.browse_button)
        layout.add_widget(self.toggle_button)
        layout.add_widget(self.log_label)
        return layout

    def display_error(self, error_message):
        self.data_gathering = False
        self.toggle_button.text = "Start gathering"  # Update the button text
        self.log_label.text += f"Error: {error_message}\n"
        self.log_label.scroll_y = 0

    def clear_error(self):
        self.log_label.text = ""

    def gather_data_thread(self):
        try:
            output_file_path = os.path.join(self.output_path, self.output_file_name)

            with open(output_file_path, 'w') as file:
                time.sleep(0.5)
                ser = serial.Serial(self.selected_port, int(self.baud_rate_val), timeout=1.5)
                while self.data_gathering:
                    data = ser.readline().decode().strip()
                    file.write(data + '\n')
                    file.flush()
                    self.log_label.text += data + '\n'
                    self.log_label.scroll_y = 0
        except Exception as e:
            self.display_error(str(e))

    def toggle_data_gathering(self, instance):
        if self.data_gathering:
            self.data_gathering = False
            Clock.schedule_once(lambda dt: setattr(self.toggle_button, 'text', "Start gathering"), 0)
            self.clear_error()  # Clear the error text
        else:
            self.data_gathering = True
            Clock.schedule_once(lambda dt: setattr(self.toggle_button, 'text', "Stop gathering"), 0)
            self.clear_error()  # Clear the error text
            self.selected_port = self.ard_port.text
            self.output_file_name = self.file_name.text + ".txt"  # Add .txt extension
            data_thread = threading.Thread(target=self.gather_data_thread)
            data_thread.start()

    def on_baud_rate_select(self, instance, value):
        self.baud_rate_val = value

    def browse_path(self, instance):
        try:
            file_chooser = FileChooserListView()
            file_chooser.path = self.output_path
            file_chooser.filters = [lambda folder, filename: filename[-4:] != '.txt']
            file_chooser.bind(on_submit=self.update_path)
            popup = Popup(title='Choose Output Path', content=file_chooser, size_hint=(None, None), size=(600, 400))
            popup.open()
        except Exception as e:
            self.display_error(str(e))

    def update_path(self, instance):
        try:
            self.output_path = instance.selection[0]
            self.file_name.text = ""  # Clear the file name field
        except Exception as e:
            self.display_error(str(e))

if __name__ == '__main__':
    DataGatherApp().run()
