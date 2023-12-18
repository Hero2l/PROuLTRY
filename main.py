import firebase_admin
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
import threading
import paramiko
from firebase import firebase
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import requests
from firebase_admin import credentials
from plyer import notification


Builder.load_file("main.kv")

# Firebase configuration
config = {
    'apiKey': "AIzaSyC5aCsGbyhI2_RvMrRADcb1KToMD5CbfZE",
    'authDomain': "raspberrypi-df44f.firebaseapp.com",
    'databaseURL': "https://raspberrypi-df44f-default-rtdb.firebaseio.com",
    'projectId': "raspberrypi-df44f",
    'storageBucket': "raspberrypi-df44f.appspot.com",
    'messagingSenderId': "177173931860",
    'appId': "1:177173931860:web:bdc5d149a3201ac57dcac1",
    'measurementId': "G-895TE2DD39"
}

# Initialize the Firebase app
firebase_db = firebase.FirebaseApplication(config['databaseURL'], None)

# Replace 'your-firebase-credentials.json' with your actual Firebase credentials JSON file
cred = credentials.Certificate(r'C:\Desktop\raspberrypi.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://raspberrypi-df44f-default-rtdb.firebaseio.com/'})

MAX_CM_VALUE = 100  # Replace with the actual maximum range of your UltrasonicSensor

class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness = 40

        # Create a direct text representation
        self.label = CoreLabel(text="0%", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = None

        # Refresh the text
        self.refresh_text()

        # Redraw on innit
        self.draw()

    def draw(self):
        with self.canvas:
            # Empty canvas instructions
            self.canvas.clear()

            # Calculate the center position of the Ellipse
            center_x = self.pos[0] + self.size[0] / 2
            center_y = self.pos[1] + self.size[1] / 2

            # Calculate the inner circle position
            inner_circle_pos = (
            center_x - self.size[0] / 2 + self.thickness / 2 + 30, center_y - self.size[1] / 2 + self.thickness / 2 + 50)

            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=(center_x - self.size[0] / 2 + 30, center_y - self.size[1] / 2 + 50), size=self.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(1, 0, 0)
            Ellipse(pos=(center_x - self.size[0] / 2 + 30, center_y - self.size[1] / 2 + 50), size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized * 360))

            # Draw the inner circle (colour should be equal to the background)
            Color(0, 0, 0)
            Ellipse(pos=inner_circle_pos, size=(self.size[0] - self.thickness, self.size[1] - self.thickness))

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            Rectangle(texture=self.label.texture, size=self.texture_size,
                      pos=(center_x - self.texture_size[0] / 2 + 30, center_y - self.texture_size[1] / 2 + 50))

    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        # Update the progress bar value
        self.value = value

        # Update textual value and refresh the texture
        self.label.text = str(int(self.value_normalized * 100)) + "%"
        self.refresh_text()

        # Draw all the elements
        self.draw()

class CircularProgressBar2(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar2, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness2 = 40

        # Create a direct text representation
        self.label2 = CoreLabel(text="0%", font_size=self.thickness2)

        # Initialise the texture_size variable
        self.texture_size2 = None

        # Refresh the text
        self.refresh_text2()

        # Redraw on innit
        self.draw2()

    def draw2(self):
        with self.canvas:
            # Empty canvas instructions
            self.canvas.clear()

            # Calculate the center position of the Ellipse
            center_x = self.pos[0] + self.size[0] / 2
            center_y = self.pos[1] + self.size[1] / 2

            # Calculate the inner circle position
            inner_circle_pos = (
            center_x - self.size[0] / 2 + self.thickness2 / 2 + 190, center_y - self.size[1] / 2 + self.thickness2 / 2 + 50)

            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=(center_x - self.size[0] / 2 + 190, center_y - self.size[1] / 2 + 50), size=self.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(1, 0, 0)
            Ellipse(pos=(center_x - self.size[0] / 2 + 190, center_y - self.size[1] / 2 + 50), size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized * 360))

            # Draw the inner circle (colour should be equal to the background)
            Color(0, 0, 0)
            Ellipse(pos=inner_circle_pos, size=(self.size[0] - self.thickness2, self.size[1] - self.thickness2))

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            Rectangle(texture=self.label2.texture, size=self.texture_size2,
                      pos=(center_x - self.texture_size2[0] / 2 + 190, center_y - self.texture_size2[1] / 2 + 50))

    def refresh_text2(self):
        # Render the label
        self.label2.refresh()

        # Set the texture size each refresh
        self.texture_size2 = list(self.label2.texture.size)

    def set_value2(self, value2):
        # Update the progress bar value
        self.value = value2

        # Update textual value and refresh the texture
        self.label2.text = str(int(self.value_normalized * 100)) + "%"
        self.refresh_text2()

        # Draw all the elements
        self.draw2()

class Main(Screen):
    label11 = None
    label12 = None
    label13 = None
    label14 = None
    label15 = None
    label16 = None
    label17 = None
    label18 = None
    label5 = None
    label6 = None
    label19 = None
    label20 = None
    label21 = None
    label22 = None
    label23 = None

    firebase_path = "flow"  # Replace 'your_path' with your Firebase database path

    # Simulated dimensions of the container in centimeters
    container_length = 30  # Replace with the actual length of the container in cm
    container_width = 20  # Replace with the actual width of the container in cm
    container_height = 30  # Replace with the actual height of the container in cm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label5 = self.ids.label5_id
        self.label6 = self.ids.label6_id
        self.connected_to_raspberry_pi = False
        self.label11 = self.ids.label11_id
        self.label12 = self.ids.label12_id
        self.label13 = self.ids.label13_id
        self.label14 = self.ids.label14_id
        self.label15 = self.ids.label15_id
        self.label16 = self.ids.label16_id
        self.label17 = self.ids.label17_id
        self.label18 = self.ids.label18_id
        self.label19 = self.ids.label19_id
        self.label20 = self.ids.label20_id
        self.label21 = self.ids.label21_id
        self.label22 = self.ids.label22_id
        self.label23 = self.ids.label23_id

        self.schedule_data_fetch(1)  # Schedule data fetch every 1 minute

        # Create CircularProgressBar instance
        self.circular_progress_bar = CircularProgressBar()
        self.ids.circular_progress_bar_container.add_widget(self.circular_progress_bar)
        self.schedule_data_fetch(1)

        self.circular_progress_bar2 = CircularProgressBar2()
        self.ids.circular_progress_bar_container2.add_widget(self.circular_progress_bar2)
        self.schedule_data_fetch(1)

    def connect_to_raspberry_pi(self):
        # Disable the "Connect" button to prevent multiple connection attempts

        def connect_thread():
            host = "192.168.100.202"
            port = 22
            username = "hero2l"
            password = "POPObeverages012"

            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.load_system_host_keys()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                self.ssh_client.connect(host, port, username, password)
                self.ids.connection_status_label.text = "Connection Status: Connected"
                self.connected_to_raspberry_pi = True
            except Exception as e:
                self.ids.connection_status_label.text = f"Connection Status: Error - {str(e)}"

        # Create and start the connection thread
        connection_thread = threading.Thread(target=connect_thread)
        connection_thread.start()

    def disconnect_to_raspberry_pi(self):
        try:
            self.ssh_client.close()
            self.ids.connection_status_label.text = "Connection Status: Disconnected"
            self.connected_to_raspberry_pi = False  # Use a different variable name here
        except Exception as e:
            self.ids.connection_status_label.text = f"Disconnection Error - {str(e)}"

    def cm_to_liters(self, cm):
        # Calculate the volume in cm³
        volume_cm3 = cm * self.container_length * self.container_width * self.container_height

        # Convert cm³ to liters (1 cm³ = 0.001 liters)
        volume_liters = volume_cm3 * 0.001

        return volume_liters

    def update_label11(self, text):
        self.label11.text = text

    def fetch_data_from_firebase1(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/FlowSensor13", None)

        if data:
            self.update_label11(f"Water Flow Sensor1: {data}")

    def update_label12(self, text):
        self.label12.text = text

    def fetch_data_from_firebase2(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/FlowSensor19", None)

        if data:
            self.update_label12(f"Water Flow Sensor2: {data}")

    def update_label13(self, text):
        self.label13.text = text

    def fetch_data_from_firebase3(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/FlowSensor5", None)

        if data:
            self.update_label13(f"Water Flow Sensor3: {data}")

    def update_label14(self, text):
        self.label14.text = text

    def fetch_data_from_firebase4(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/FlowSensor6", None)

        if data:
            self.update_label14(f"Water Flow Sensor3: {data}")

    def update_label15(self, text):
        self.label15.text = text

    def fetch_data_from_firebase5(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Relay", None)

        if data:
            self.update_label15(f"Water Pump: {data}")

    def update_label16(self, text):
        self.label16.text = text

    def fetch_data_from_firebase6(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/UltrasonicSensor", None)

        if data:
            ultrasonic_data_cm = data  # Replace 'ultrasonic_data_cm' with the actual data variable name
            # Convert to liters
            ultrasonic_data_liters = self.cm_to_liters(ultrasonic_data_cm)
            self.update_label16(f"Water Level {ultrasonic_data_liters:.2f} Liters")

    def update_label17(self, text):
        self.label17.text = text

    def fetch_data_from_firebase7(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Water Detected", None)

        if data:
            self.update_label17(f"Water Sensor: {data}")

    def update_label18(self, text):
        self.label18.text = text

    def fetch_data_from_firebase8(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/WaterLevel", None)

        if data:
            self.update_label18(f"Water Level: {data}")

    def update_label19(self, text):
        self.label19.text = text

    def fetch_data_from_firebase10(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Load Cell 1", None)

        if data:
            self.update_label19(f"Feed Weight 1: {data}")

    def update_label20(self, text):
        self.label20.text = text

    def fetch_data_from_firebase11(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Load Cell 2", None)

        if data:
            self.update_label20(f"Feed Weight 2: {data}")

    def update_label21(self, text):
        self.label21.text = text

    def fetch_data_from_firebase12(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Total Reading", None)

        if data:
            self.update_label21(f"Feed Weight Overall: {data}")

    def update_label22(self, text):
        self.label22.text = text

    def fetch_data_from_firebase13(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Relay2", None)

        if data:
            self.update_label22(f"Dc Motor: {data}")

    def update_label23(self, text):
        self.label23.text = text

    def fetch_data_from_firebase14(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/BuzzerStatus", None)

        if data:
            self.update_label23(f"Feed Level: {data}")

        if data and data.lower() == "feed level is low":
            self.show_feed_level_notification()

    def show_feed_level_notification(self):
        title = "Feed Level Warning"
        message= "The Feed Level is Low. Please Refill the feed"
        self.show_notification(title,message)

    def show_notification(self, title, text):
        notification.notify(
            title=title,
            message=text,
            app_name=self.name,
        )
    def update_label5(self, text):
        self.label5.text = text

    def update_label6(self, text):
        self.label6.text = text

    def fetch_data_from_firebase9(self, dt):
        # Fetch data for the "UltrasonicSensor" key within the "flow" key from Firebase
        data = firebase_db.get(f"{self.firebase_path}/Relay", None)

        if data:
            self.update_label5(f"Water Pump Status: {data}")

    def on_water_pump(self):
        # Check if connected to the Raspberry Pi
        if self.connected_to_raspberry_pi:
            try:
                # Make an HTTP request to turn on the water pump
                response = requests.get("http://192.168.100.202:5000/relay/on")
                if response.status_code == 200:
                    self.update_label5("Water Pump turned on")
                else:
                    self.update_label5("Failed to turn on Water Pump")
            except Exception as e:
                self.update_label5(f"Error: {str(e)}")
        else:
            self.update_label5("Not connected to Raspberry Pi. Please connect first.")

    def off_water_pump(self):
        # Check if connected to the Raspberry Pi
        if self.connected_to_raspberry_pi:
            try:
                # Make an HTTP request to turn off the water pump
                response = requests.get("http://192.168.100.202:5000/relay/off")
                if response.status_code == 200:
                    self.update_label5("Water Pump turned off")
                else:
                    self.update_label5("Failed to turn off Water Pump")
            except Exception as e:
                self.update_label5(f"Error: {str(e)}")
        else:
            self.update_label5("Not connected to Raspberry Pi. Please connect first.")

    def on_dc_motor(self):
        # Check if connected to the Raspberry Pi
        if self.connected_to_raspberry_pi:
            try:
                # Make an HTTP request to turn on the water pump
                response = requests.get("http://192.168.100.202:5000/relay2/on")
                if response.status_code == 200:
                    self.update_label6("DC Motor turned on")
                else:
                    self.update_label6("Failed to turn on DC Motor")
            except Exception as e:
                self.update_label6(f"Error: {str(e)}")
        else:
            self.update_label6("Not connected to Raspberry Pi. Please connect first.")

    def off_dc_motor(self):
        # Check if connected to the Raspberry Pi
        if self.connected_to_raspberry_pi:
            try:
                # Make an HTTP request to turn on the water pump
                response = requests.get("http://192.168.100.202:5000/relay2/off")
                if response.status_code == 200:
                    self.update_label6("DC Motor turned off")
                else:
                    self.update_label6("Failed to turn off DC Motor")
            except Exception as e:
                self.update_label6(f"Error: {str(e)}")
        else:
            self.update_label6("Not connected to Raspberry Pi. Please connect first.")

    def update_from_firebase(self, dt):
        # Retrieve data from Firebase
        sensor_data = firebase_db.get(f"{self.firebase_path}/UltrasonicSensor", None)
        sensor_data2 = firebase_db.get(f"{self.firebase_path}/UltrasonicSensor2", None)

        # Assuming 'sensor_data' is an integer representing the progress value
        if sensor_data is not None:
            self.circular_progress_bar.set_value(sensor_data)
        if sensor_data2 is not None:
            self.circular_progress_bar2.set_value2(sensor_data2)

    def schedule_data_fetch(self, interval_minutes):
        # Initial fetch
        self.fetch_data_from_firebase1(None)
        self.fetch_data_from_firebase2(None)
        self.fetch_data_from_firebase3(None)
        self.fetch_data_from_firebase4(None)
        self.fetch_data_from_firebase5(None)
        self.fetch_data_from_firebase6(None)
        self.fetch_data_from_firebase7(None)
        self.fetch_data_from_firebase8(None)
        self.fetch_data_from_firebase9(None)
        self.fetch_data_from_firebase10(None)
        self.fetch_data_from_firebase11(None)
        self.fetch_data_from_firebase12(None)
        self.fetch_data_from_firebase13(None)
        self.fetch_data_from_firebase14(None)

        # Schedule subsequent fetches
        Clock.schedule_interval(self.fetch_data_from_firebase1, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase2, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase3, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase4, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase5, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase6, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase7, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase8, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase9, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase10, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase11, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase12, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase13, interval_minutes * 120)
        Clock.schedule_interval(self.fetch_data_from_firebase14, interval_minutes * 120)
        Clock.schedule_interval(self.update_from_firebase, interval_minutes * 120)
class MyApp(MDApp):
    def build(self):
        self.title = "Poultry System"
        Window.size = (360, 800)
        self.theme_cls.theme_style = "Dark"
        self.sm = ScreenManager()

        main = Main(name="Main")
        self.sm.add_widget(main)
        self.sm.current = "Main"

        return self.sm

    def animate(self, dt):
        # You can keep your existing animation logic or modify it as needed
        self.sm.get_screen("Main").update_from_firebase(dt)

    def on_start(self):
        Clock.schedule_interval(self.animate, 10)


if __name__ == "__main__":
    MyApp().run()