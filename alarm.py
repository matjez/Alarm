from datetime import datetime, timedelta
import json
import time

class Alarm():
    alarms = {}
    alarms_converted = {}
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday",]

    def __init__(self) -> None:
        self.convert_alarms()

    def convert_alarms(self):
        if len(Alarm.alarms) > 0:
            for name in Alarm.alarms.keys():
                tmp_date = Alarm.alarms[name]             

                for day in Alarm.days:
                    if day in tmp_date["days"]:
                        current_date = datetime.now()
                        tmp_time = datetime(current_date.year,current_date.month,current_date.day,int(tmp_date["hour"]),int(tmp_date["minute"]))

                        for _ in range(7):
                            if tmp_time.strftime("%A") == day:
                                alarm_name = name + "_" + day
                                current_datetime = tmp_time

                                if (tmp_time - current_date) < timedelta(days=0):
                                    Alarm.alarms_converted[alarm_name] = (current_datetime + timedelta(7))
                                else:
                                    Alarm.alarms_converted[alarm_name] = current_datetime

                            tmp_time = tmp_time + timedelta(days=1) 
                                                
    def set_alarm(self,name, days, hour, minute):
        Alarm.alarms[name] = {"days":days, "hour": int(hour), "minute": int(minute)}
        self.convert_alarms()

    def remove_alarm(self, alarm_name):
        Alarm.alarms[alarm_name].remove()
        self.convert_alarms()

    def show_closest_alarm(self):
        alarms_dict = list(Alarm.alarms_converted.copy().keys())
        current_time = datetime.now() 

        closest_alarm_name = alarms_dict[0]
        closest_alarm = Alarm.alarms_converted[alarms_dict[0]] - current_time

        for alarm_name in alarms_dict:
            tmp_alarm = Alarm.alarms_converted[alarm_name] - current_time

            if closest_alarm > tmp_alarm and tmp_alarm > timedelta(days=0):
                closest_alarm_name = alarm_name
                closest_alarm = Alarm.alarms_converted[alarm_name] - current_time
                
        return closest_alarm_name  


    @classmethod
    def update_json_alarms(cls):
        json_alarms = json.dumps(cls.alarms, indent = 4)
        with open("data/alarms.json","w") as f:
            f.write(json_alarms)     

    @classmethod
    def show_alarms(cls):
        with open("data/alarms.json","r") as f:
            json_alarms = json.loads(f.read())
            Alarm.alarms = json_alarms
            return json_alarms
