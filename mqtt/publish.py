from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


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
print("Publishing message to AWS IoT Broker...")
MQTTclient.publish(
    topic="awsiot/test",
    QoS=1,
    payload="Hello from quil-lm",
)
