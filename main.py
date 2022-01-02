import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import ttk
from threading import *
from queue import Queue

#definitions
broker_address="localhost" 
port = 1883
topicHouseMainLight = "house/Light/main-light"
topicTemperaturSensor = "house/temperature/sensor1"

q = Queue()


class Client():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(broker_address, port)
        self.client.subscribe(topicTemperaturSensor)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):      
        q.put(str(msg.payload))
        print("\n" + topicTemperaturSensor + " " + str(msg.payload))        
                
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
        self.geometry('400x400')

        # label
        self.labelConnection = ttk.Label(self, text='You are connected to MQTT Broker: ' + broker_address)
        self.labelConnection.pack()

        self.labelReceivedMsgData = ttk.Label(self)
        self.labelReceivedMsgData.pack()

        # entry
        self.entryPublishMessage = ttk.Entry(self)
        self.entryPublishMessage.pack()

        # button
        self.buttonPublishMsg = ttk.Button(self, text="publish")
        self.buttonPublishMsg['command'] = self.Publish #Fick Dich Tkinter, wieso kann in nd glei command=self.publish schreiben :)
        self.buttonPublishMsg.pack()

    def Publish(self):
        self.client.PublishMessage(self.entryPublishMessage.get())
        print(self.entryPublishMessage.get())


def loop():
    app = Application()
    
    while True:
        while not q.empty():
            message = q.get()
            if message is None:
                continue
            else:
                app.labelReceivedMsgData.config(text=message)
            
        app.after(10, app.update())


def main():
    client = Client()
    client.ReceiveMessage()
    loop()

    
    
if __name__ == "__main__":
    main()
