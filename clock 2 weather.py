import tkinter as tk
from datetime import datetime
import time
import threading
import json
import pygame
import requests


class AlarmClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alarmclock")

        self.time_label = tk.Label(self.root, text="", font=('Helvetica', 40))
        self.time_label.pack()

        self.weather_label = tk.Label(self.root, text="", font=('Helvetica', 20))
        self.weather_label.pack()

        self.alarm_time = tk.StringVar()
        self.set_alarm_frame = tk.Frame(self.root)
        self.set_alarm_frame.pack()
        self.alarm_entry = tk.Entry(self.set_alarm_frame, textvariable=self.alarm_time)
        self.alarm_entry.pack(side=tk.LEFT)

        self.set_button = tk.Button(self.set_alarm_frame, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(side=tk.LEFT)

        self.snooze_button = tk.Button(self.root, text="Snooze", command=self.snooze_alarm)
        self.snooze_button.pack()

        self.update_time()
        self.load_alarm()
        self.update_weather()
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def update_weather(self):
        weather = self.get_weather()
        self.weather_label.config(text=weather)
        self.root.after(600000, self.update_weather)

    def get_weather(self):
        api_key = "YOUR_API_KEY"
        city = "London"  
        url = f"https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=2ecba0dbb81830631c384af04a3b734d"

        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                weather = f"{city}: {weather_description}, {temperature}°C"
                return weather
            else:
                return "Error fetching weather"
        except Exception as e:
            return f"Error: {e}"

    def set_alarm(self):
        alarm_time = self.alarm_time.get()
        print(f"Alarm set for {alarm_time}")
        self.save_alarm(alarm_time)
        threading.Thread(target=self.alarm_thread, args=(alarm_time,)).start()

    def alarm_thread(self, alarm_time):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == alarm_time:
                self.play_alarm_sound()
                break
            time.sleep(1)

    def play_alarm_sound(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("Powerhouse-Vibe-MassTamilan.dev(1)")
            pygame.mixer.music.play(loops=0)
            print("Time to wake up")
        except Exception as e:
            print(f"Error playing sound: {e}")

    def snooze_alarm(self):
        snooze_time = 1 * 60  # 1 minute snooze time
        print("Snooze for 1 minute")
        threading.Thread(target=self.snooze_thread, args=(snooze_time,)).start()

    def snooze_thread(self, snooze_time):
        time.sleep(snooze_time)
        self.play_alarm_sound()

    def save_alarm(self, alarm_time):
        with open("alarm.json", 'w') as file:
            json.dump({"alarm_time": alarm_time}, file)

    def load_alarm(self):
        try:
            with open("alarm.json", 'r') as file:
                alarm_data = json.load(file)
                self.alarm_time.set(alarm_data["alarm_time"])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = AlarmClock()
    app.root.mainloop()