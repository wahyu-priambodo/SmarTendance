import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def callback(self, params, packet):
    print("Received message from AWS IoT Core")
    print("Topic: " + packet.topic)
    print("Payload: ", (packet.payload))


MQTTclient = AWSIoTMQTTClient("LM-key")  # Random Key
MQTTclient.configureEndpoint(
    "a2pr7kvz6d0wr2-ats.iot.ap-southeast-2.amazonaws.com", 8883
)

MQTTclient.configureCredentials(
    "./.cert/AmazonRootCA1.crt",
    "./.cert/private.pem.key",
    "./.cert/certificate.pem.crt",
)

MQTTclient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
MQTTclient.configureDrainingFrequency(2)  # Draining: 2 Hz
MQTTclient.configureConnectDisconnectTimeout(10)  # 10 sec
MQTTclient.configureMQTTOperationTimeout(5)  # 5 sec

print("Connecting to AWS IoT Broker...")
MQTTclient.connect()
MQTTclient.subscribe("awsiot/test", 1, callback)
print("Waiting for messages...")

while True:
    time.sleep(5)
