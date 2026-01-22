from kafka import KafkaConsumer
import json
import config
import psycopg2

def deserialization(serialized): #полученные из топика данные десериализуем (байты -> начальный формат)
    return json.loads(serialized.decode('utf-8'))

def validate_table_name(table_name): #работает - проверено
    if table_name == None:
        return False
    return True

def validate_data(list_data): #работает - проверено
    if list_data == None:
        print('Validation: error: empty data')
        return False
    elif not (type(list_data) is list and len(list_data) > 0):
        print('Validation: error')
        return False
    return True

def db_connect():
    return psycopg2.connect(dbname=config.DB_DATABASE, host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, port=config.DB_PORT)

def exist_table(table_name, cursor):
    cursor.execute(f'SELECT * FROM {config.DB_DATABASE}.TABLES WHERE TABLE_NAME = {table_name};')
    if(cursor.fetchall()):
        return True
    else:
        print('table dont exist')
        return False

def type_field(rows,columns): #работает - проверено
    type_list = []
    for i in range(1, len(columns)):
        status = 'INTEGER'
        for j in range(0, len(rows)):
            if(type(rows[j][i]) is str):
                status = 'VARCHAR(255)'
                break
            elif (type(rows[j][i]) is float):
                status = 'DOUBLE'
        type_list.append(status)
    return type_list


def create_table(table_name,columns,types):
    sql = f'CREATE TABLE {table_name} (id SERIAL PRIMARY KEY'
    k = 0
    for i in columns:
        if not (i == 'id'):
            sql += f', {i} {types[k]}'
            k += 1
    sql += ');'
   # print(sql)
    #cursor.execute(sql)
    
def insert_data(table_name, columns, row,type_list):
    sql = f"INSERT INTO {table_name} ("
    k = 0
    for i in columns:
        if not (i == 'id'):
            sql += f'{i}, '
    sql = sql[:-2]
    sql += ") VALUES ("
    for i in range(1,len(row)):
        if type_list[i-1] == 'VARCHAR(255)':
            sql += f"'{row[i]}', "
        else:
            sql += f"{row[i]}, "
    sql = sql[:-2] + ');'
    print(sql)
    #cursor.execute(sql)

def event_listening(data):
    table_name = data['table_name']
    columns = data['columns']
    rows = data['rows']
    if  validate_table_name(table_name) and validate_data(columns) and validate_data(rows):
        print('Data is consistent')
    if not exist_table(table_name,cursor):
        create_table(table_name)
       # insert_data(columns, row)
    else:
       # insert_data(columns, row)
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
    #connector = db_connect()
    #cursor = connector.cursor()
    #connector.autocommit = True
    type_field([[1,2,4],[2,6.0,8]],['id','o','a'])
    print(validate_data(None))
    print(validate_table_name(None))
    print(validate_data(3))
    print(validate_data([3]))
    create_table('openn', ['id','count','size'],type_field([[1,2,2.0],[2,2,1],[3,5,12.9]],['id','count','size']))
    insert_data('openn', ['id','count','size'], [1,2,2.0], type_field([[1,2,2.0],[2,2,1],[3,5,12.9]],['id','count','size']))
    #consume()
    #cursor.close()  # закрываем курсор
    #connector.close()