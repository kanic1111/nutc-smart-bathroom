import paho.mqtt.subscribe as subscribe

broker_ip = "10.20.0.19"
broker_port = 1883

def set_mqtt(broker_user_ip, broker_user_port=1883):
    global broker_ip, broker_port
#    print(broker_user_ip, broker_user_port)
    broker_ip = broker_user_ip
    broker_port = broker_user_port

def create_Subscribe(listen_topic):
#    print("mqtt_server = %s, mqtt_port = %s" %(broker_ip, broker_port))
    msg = subscribe.simple(listen_topic, hostname=broker_ip, port=broker_port, keepalive=15)
#    print("Topic = %s, Payload = %s" % (msg.topic, msg.payload.decode('utf-8')))
    return msg.payload.decode('utf-8')

# def get_Co():
#     return create_Subscribe("EtherIO/CO")

# def get_Co2():
#     return create_Subscribe("EtherIO/CO2")

def get_Humidity():
    return create_Subscribe("PIR231/RH")

def get_Temperature():
    return create_Subscribe("PIR231/TC")

def get_DewPoint():
    return create_Subscribe("PIR231/DC")

def get_PIR():
    return create_Subscribe("PIR231/PIR")