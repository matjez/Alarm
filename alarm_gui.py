from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from alarm import *
from threading import Thread
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.textinput import TextInput

class ColorTextInput(TextInput):

    def changetored(self):
        if self.text != "Edit me !":
            self.foreground_color = (0.93,0.80,1.00)

class AlarmGUI(BoxLayout, Alarm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.show_alarms()
        self.ids["hour"].text = "00"
        self.ids["minute"].text = "00"
        self.ids["alarm_name_input"].text = "Alarm1"
        self.ids["hour"].bind(text=self.validate_time)
        self.ids["minute"].bind(text=self.validate_time)
        self.ids["alarm_name_input"].bind(text=self.validate_alarm_name)
        self.closest_alarm_name = ""

        self.dialog = None
        self.selected_days = []
        # self.set_alarm("Moj alarm 1", ["Monday","Sunday","Tuesday"], "12", "00")           #ustawienie nowego alarmu
        self.convert_alarms()

        new_thread = Thread(target=self.alarm_counter)
        new_thread.daemon = True
        new_thread.start()

    def show_alert_dialog(self):

        layout = GridLayout(cols = 1, padding = 10)
  
        popupLabel = Label(text = "Wake up!")
        popupLabel.font_size = 64
        popupLabel.size_hint = (0.5,0.6)
        closeButton = Button(text = "Ok")
        closeButton.font_size = 48
        closeButton.size_hint = (0.5,0.2)
        closeButton.background_color = [0.10,0.00,0.18, 1]
        closeButton.bind(on_release = self.confirm_alarm)

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        popup = Popup(title ='Alarm',
                      content = layout,
                      separator_color = [.9, .4, .2, 1],
                      background_color = [0.10,0.00,0.18, 1])  
        popup.open()   
        closeButton.bind(on_press = popup.dismiss)   

    def set_days(self, instance):
        if instance.text:

            week_day = ""
            for id, widget in self.ids.items():
                if widget.__self__ == instance:
                    week_day = id

            if week_day == "":
                return
                
            if week_day in self.selected_days:
                self.selected_days.remove(week_day)
                instance.background_color = (0.33,0.00,0.75)

            else:
                self.selected_days.append(week_day)
                instance.background_color = (0.9,0,0.9)

    def alarm_counter(self):  
        time.sleep(0.5)
        while True:
            time.sleep(1)
            alarms_copy = Alarm.alarms_converted.copy()
            alarms_copy2 = Alarm.alarms.copy()

            if self.closest_alarm_name != "":
                splitted = self.closest_alarm_name.split(".")
                date_obj = datetime.strptime(
                    splitted[1], '%Y-%m-%d %H:%M:%S')

                diff = date_obj - datetime.now()
                if diff < timedelta(days=0):
                    print(self.closest_alarm_name)
                    self.convert_alarms()
                    self.play_sound()
                    self.show_alert_dialog()
                    
                    self.closest_alarm_name = ""

                    continue

        
            self.closest_alarm_name = self.show_closest_alarm()

            if self.closest_alarm_name != "":
                
                diff_converted = str(alarms_copy[self.closest_alarm_name] - datetime.now())
                diff_converted = diff_converted.replace(","," -")
                diff_converted = diff_converted.split(".")

                print(str(diff_converted[0]))

                self.ids["screen"].text = diff_converted[0]

    def validate_time(self,instance, value):
        if len(value) > 0 and len(value) <= 2 and value.isdigit():
            int_val = int(value)
        else:
            instance.text = instance.text[:-1]
            return

        if instance.text == "hour":       
            if int_val < 0 or int_val > 23:
                instance.text = instance.text[:-1]

        else:
            if int_val < 0 or int_val > 59:
                instance.text = instance.text[:-1]

    def validate_alarm_name(self,instance, value):
        value = value.replace(" ","")
        value = value.replace("-","")
        value = value.replace("_","")
        
        if not value.isalnum():
            instance.text = instance.text[:-1]


    def set_alarm_button(self):

        hour = self.ids["hour"].text
        minute = self.ids["minute"].text
        alarm_name_input = self.ids["alarm_name_input"].text

        if len(self.selected_days) > 0 and hour != "" and minute != "": 
            self.set_alarm(alarm_name_input,self.selected_days,hour,minute)
            self.reset_settings()

    def reset_settings(self):
        self.ids["hour"].text = "00"
        self.ids["minute"].text = "00"
        self.ids["alarm_name_input"].text = "Alarm1"

        for day in Alarm.days:    
            self.ids[day].background_color = (0.33,0.00,0.75)

        self.selected_days = []

    def time_up(self,instance):
        if instance in self.ids.values():
            instance_id = list(self.ids.keys())[list(self.ids.values()).index(instance)]  

            if instance_id == "hour_up":
                value = int(self.ids["hour"].text)

                if value == 23:
                    self.ids["hour"].text = "00"
                else:
                    if value < 9:
                        self.ids["hour"].text = "0" + str(value + 1)
                    else:
                        self.ids["hour"].text = str(value + 1)

            elif instance_id == "hour_down":
                value = int(self.ids["hour"].text)
                if value == 0:
                    self.ids["hour"].text = "23"
                else:
                    if value <= 10:
                        self.ids["hour"].text = "0" + str(value - 1)
                    else:
                        self.ids["hour"].text = str(value - 1)

            elif instance_id == "minute_up":
                value = int(self.ids["minute"].text)
                if value == 59:
                    self.ids["minute"].text = "00"
                else:
                    if value < 9:
                        self.ids["minute"].text = "0" + str(value + 1)
                    else:
                        self.ids["minute"].text = str(value + 1)

            elif instance_id == "minute_down":
                value = int(self.ids["minute"].text)
                if value == 0:
                    self.ids["minute"].text = "59"
                else:
                    if value <= 10:
                        self.ids["minute"].text = "0" + str(value - 1)
                    else:
                        self.ids["minute"].text = str(value - 1)


    def play_sound(self):
        self.sound = SoundLoader.load('ringtone_1.mp3')

        alarm_info = self.closest_alarm_name.split(".")
        alarm_name = alarm_info[0]
        weekday = alarm_info[2]
        
        Alarm.alarms[alarm_name]["days"].remove(weekday)
        
        del Alarm.alarms_converted[self.closest_alarm_name]

        self.convert_alarms()

        if self.sound:
            self.sound.loop = True
            self.sound.play()

    def confirm_alarm(self,x):
        try:
            self.sound.stop()
            self.sound.unload()
        except:
            pass

class GUIApp(App):
  
    def build(self):
        self.icon = "appicon.jpg"
        self.title = 'Alarm'
        return AlarmGUI()
  
if __name__ == "__main__":
    Config.set('graphics', 'resizable', True)
    app = GUIApp()
    Window.size = (600, 800)
    Window.maxsize = (600, 800)
    app.run()
