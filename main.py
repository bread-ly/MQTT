import paho.mqtt.client as mqtt
import time

broker_address="localhost" #defining Server
topicHouseMainLight = "house/Light/main-light"
topicTemperaturSensor = "house/temperature/sensor1"
port = 1883

def on_message(client, userdata, msg):
    print("\n" + topicTemperaturSensor + " " + str(msg.payload))

client = mqtt.Client()
client.connect(broker_address, port)
client.subscribe(topicTemperaturSensor)
client.loop_start()

def ReceiveMessage():
    client.on_message = on_message
    
def PublishMessage():
    client.publish(topicHouseMainLight, input("Hier Eingabe " + "\n->"))

def loop():
    while 1:
        ReceiveMessage()
        PublishMessage()
        
def main():
    loop()
        
if __name__ == "__main__":
    main()
