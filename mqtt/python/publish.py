# Using AWS IOT as MQTT Broker
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


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

print("Connecting to AWS IoT Broker...")
MQTTclient.connect()
print("Publishing message to AWS IoT Broker...")

# Set topic to 'awsiot/test' and publish a message
MQTTclient.publish(
    topic="awsiot/test",
    QoS=1,
    payload="Hello from quil-lm",
)
