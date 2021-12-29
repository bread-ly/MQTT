import paho.mqtt.client as mqtt
import time

broker_address="localhost" #defining Server
topicHouseMainLight = "house/Light/main-light"
topicTemperaturSensor = "house/temperature/sensor1"
port = 1883

class Client():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(broker_address, port)
        self.client.subscribe(topicTemperaturSensor)
        self.client.loop_start()

    def on_message(self, Client, Userdata, msg):
        print("\n" + topicTemperaturSensor + " " + str(msg.payload))

    def ReceiveMessage(self):
        self.client.on_message = self.on_message
        
    def PublishMessage(self):
        self.client.publish(topicHouseMainLight, input("Hier Eingabe " + "\n->"))

    def loop(self):
        while 1:
            self.ReceiveMessage()
            self.PublishMessage()
        
def main():
    client = Client()
    client.loop()
        
if __name__ == "__main__":
    main()
