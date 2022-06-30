import base64
import json
import os
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('pruebas-pubsub-systerminal')


def publisher_cf(request):
    data = request.data

    if data is None:
        print('request.data is empty')
        return ('request.data is empty', 400)

    print(f'request data: {data}')
    
    data_json = json.loads(data)                                        # turn the string into a dictionary
    print(f'json = {data_json}')

    sensor_name = data_json['sensorName']
    temperature = data_json['temperature']
    humidity = data_json['humidity']
    
    print(f'sensor_name = {sensor_name}')
    print(f'temperature = {temperature}')
    print(f'humidity = {humidity}')

    ###############################
    # move the data to Pubsub!

    topic_path = 'projects/pruebas-pubsub-systerminal/topics/topic-cf'                    # Pubsub topic path

    message_json = json.dumps({
        'data': {'message': 'sensor readings!'},
        'readings': {
            'sensorName': sensor_name,
            'temperature': temperature,
            'humidity': humidity
        }
    })
    message_bytes = message_json.encode('utf-8')

    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()                                         # verify that the publish succeeded
    except Exception as e:
        print(e)
        return (e, 500)

    return ('Message received and published to Pubsub', 200)

