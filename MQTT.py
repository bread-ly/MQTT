import paho.mqtt.client as mqtt
from tkinter import *

#definitions
messageReceived = "dwdwe"

window = Tk()

lbl_message = Label(window, text=messageReceived)
lbl_message.grid(column=0, row=0)




broker = '127.0.0.1'
port = 1883
topic = "python/ehre"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    messageReceived=(str(msg.topic)+" "+str(msg.payload))
    print(messageReceived)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

input("ehre\n")
client.publish(topic, "ehrenmänner")
input("asdf")

window.mainloop()