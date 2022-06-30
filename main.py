import base64
import json
import os
from google.cloud import pubsub_v1
from google.cloud import storage

PROJECT_ID = os.getenv('pruebas-pubsub-systerminal')


def publisher_cf(event, context):

    ##############################
    # read data from Bucket!
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(f'{PROJECT_ID}-input-data')
    blob = bucket.get_blob(event['name'])

#    destination_file = 'file.json'
#    blob.download_to_filename(destination_file)

    with open(blob, encoding="utf-8") as infile:
        data_json = json.loads(infile)

    if data_json is None:
        data_json = 'Data is empty'

    sensor_name = data_json['sensorName']
    temperature = data_json['temperature']
    humidity = data_json['humidity']
    

    ###############################
    # move the data to Pubsub!

    publisher = pubsub_v1.PublisherClient()
    topic_path = f'projects/{PROJECT_ID}/topics/topic-cf'

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
        publish_future.result() # verify that the publish succeeded
    except Exception as e:
        print(e)
        return (e, 500)

    print('Message received from Bucket and published to Pubsub')

