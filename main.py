import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import ttk
#from threading import *
from queue import Queue

import random
import time

#========definitions========#
broker_address="172.104.234.24" 
port = 1883
topicHouseMainLight = "house/Light/main-light"
topicTemperaturSensor = "house/temperature/sensor1"
benutzer = "lukas"
passwort = "lukas"

q = Queue()


class Client():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(benutzer, password=passwort)
        self.client.connect(broker_address, port)
        self.client.subscribe(topicTemperaturSensor)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):      
        q.put(str(msg.payload))
        #print("\n" + topicTemperaturSensor + " " + str(msg.payload))        
                
    def ReceiveMessage(self):
        self.client.on_message = self.on_message
        
    def PublishMessage(self, msgData):
        self.client.publish(topicHouseMainLight, msgData)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.BuildApp()
        
    def BuildApp(self):
        # configure the root window
        self.title('MQTT Explorer aber halt nd so gut')
        self.geometry('400x200')

        # label
        self.labelConnection = ttk.Label(self, text='You are connected to MQTT Broker: ' + broker_address, font=("Arial", 10))
        self.labelConnection.pack()

        self.labelSpacer = ttk.Label(self, text="===========================================")
        self.labelSpacer.pack()

        self.labelReceivedMsgData = ttk.Label(self, text="Sensor Reading: ")
        self.labelReceivedMsgData.pack()

        self.labelSpacer1 = ttk.Label(self, text="===========================================")
        self.labelSpacer1.pack()

        self.labelTopicLight = ttk.Label(self, text="Controll Topic: " + topicHouseMainLight)
        self.labelTopicLight.pack()

        # Button
        self.buttonPublishMsgOn = ttk.Button(self, text="ON")
        self.buttonPublishMsgOn['command'] = lambda: self.Publish("on")
        self.buttonPublishMsgOn.pack()

        self.buttonPublishMsgOff = ttk.Button(self, text="OFF")
        self.buttonPublishMsgOff['command'] = lambda: self.Publish("off")
        self.buttonPublishMsgOff.pack()


    def Publish(self, msg):
        self.client.PublishMessage(msg)
        

def loop():
    app = Application()
    time = time
    while True:

        while not q.empty():
            message = q.get()
            if message is None:
                continue
            else:
                app.labelReceivedMsgData.config(text="Sensor Reading: " + message.translate({98: None, 39: None}) + "°")
                                                                                            #Look up ASCII Table
            
        app.after(10, app.update())
        #app.after(5000, app.update_idletasks())


def main():
    client = Client()
    client.ReceiveMessage()
    loop()

    
if __name__ == "__main__":
    main()
