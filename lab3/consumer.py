from kafka import KafkaConsumer
import json
import config

def deserialization(serialized): #полученные из топика данные десериализуем (байты -> начальный формат)
    return json.loads(serialized.decode('utf-8'))

def event_listening(data):
    pass

async def consume():
    try:
        consumer = KafkaConsumer(config.TABLE_TOPIC, 
        bootstrap_servers = [f'{config.HOST}:{config.PORT}'],
        value_deserializer = lambda m:deserialization(m),group_id='modern-learning',auto_offset_reset='latest',
        enable_auto_commit=True)

        for message in consumer:
            try:
                    data = message.value
                    print(f"Получено сообщение:")
                    print(f"  Данные: {data}")
                    print("-" * 50)
                    
                    event_listening(data)
                    
            except json.JSONDecodeError as e:
                    print(f"Ошибка десериализации: {e}")
            except Exception as e:
                    print(f"Ошибка обработки сообщения: {e}")
    except KeyboardInterrupt:
        print("Прерывание")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        consumer.close()

if __name__ == '__main__':
    consume()