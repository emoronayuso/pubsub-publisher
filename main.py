import base64
import json
import os
from google.cloud import pubsub_v1
from google.cloud import storage

BUCKET = 'pruebas-pubsub-systerminal-input-data'
TOPIC_PATH = 'projects/pruebas-pubsub-systerminal/topics/topic-cf'

def publisher_cf(event, context):

    ##############################
    # read data from Bucket!
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)
    
    blob = bucket.get_blob(event['name'])
    data_json_str = blob.download_as_string()
    data_json = json.loads(data_json_str)

    sensor_id = data_json['sensorId']
    temperature = data_json['temperature']
    humidity = data_json['humidity']
    

    ###############################
    # move the data to Pubsub!

    publisher = pubsub_v1.PublisherClient()

    message_json = json.dumps({
        'data': {'message': 'sensor readings!'},
        'readings': {
            'sensorId': sensor_id,
            'temperature': temperature,
            'humidity': humidity
        }
    })
    message_bytes = message_json.encode('utf-8')

    try:
        publisher.publish(TOPIC_PATH, data=message_bytes)
    except Exception as e:
        print(e)
        return (e, 500)

    print('Message received from Bucket and published to Pubsub')

