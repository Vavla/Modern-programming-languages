from kafka import KafkaConsumer
import json

def deserialization(serialized): #полученные из топика данные десериализуем (байты -> начальный формат)
    return json.loads(serialized)
