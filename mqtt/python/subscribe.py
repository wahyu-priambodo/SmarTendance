# Using AWS IOT as MQTT Broker
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# Callback function to print message received from AWS IoT Core
def callback(self, params, packet):
    print("Received message from AWS IoT Core")
    print("Topic: " + packet.topic)
    print("Payload: ", (packet.payload))


MQTTclient = AWSIoTMQTTClient("LM-key")  # Random Key
MQTTclient.configureEndpoint(
    "a2pr7kvz6d0wr2-ats.iot.ap-southeast-2.amazonaws.com",
    8883,
)

# Certificate with RootCA, Private Key, and Certificate
MQTTclient.configureCredentials(
    "./.cert/quil-lm/AmazonRootCA1.crt",
    "./.cert/quil-lm/private.pem.key",
    "./.cert/quil-lm/certificate.pem.crt",
)

MQTTclient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
MQTTclient.configureDrainingFrequency(2)  # Draining: 2 Hz
MQTTclient.configureConnectDisconnectTimeout(10)  # 10 sec
MQTTclient.configureMQTTOperationTimeout(5)  # 5 sec

# Set topic to 'awsiot/test' and subscribe to a message
print("Connecting to AWS IoT Broker...")
MQTTclient.connect()
MQTTclient.subscribe(
    "awsiot/pub",
    1,
    callback,
)
print("Waiting for messages...")

# Wait for messages by looping infinitely
while True:
    time.sleep(5)
