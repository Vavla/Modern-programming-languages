from kafka import KafkaConsumer
import json
import config
import psycopg2

def deserialization(serialized): #полученные из топика данные десериализуем (байты -> начальный формат)
    return json.loads(serialized.decode('utf-8'))

def validate_table_name(table_name):
    if table_name == None:
        return False
    return True

def validate_data(list_data):
    if list_data == None:
        print('Validation: error: empty data')
        return False
    elif not (type(list_data) is list and len(list_data) > 0):
        print('Validation: error')
        return False
    return True

def event_listening(data):
    table_name = data['table_name']
    columns = data['columns']
    rows = data['rows']
    if  validate_table_name(table_name) and validate_data(columns) and validate_data(rows):
        print('Data is consistent')
    
    pass

def consume():
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
    print(validate_data(None))
    print(validate_table_name(None))
    print(validate_data(3))
    print(validate_data([3]))
    #consume()