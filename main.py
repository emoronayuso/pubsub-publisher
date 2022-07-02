import base64
import json
import os
from google.cloud import pubsub_v1
from google.cloud import storage

#PROJECT_ID = os.getenv('pruebas-pubsub-systerminal')


def publisher_cf(event, context):

    ##############################
    # read data from Bucket!
    
    storage_client = storage.Client()
    bucket = storage_client.bucket('pruebas-pubsub-systerminal-input-data')

#    blob_file = bucket.get_blob(event['name'])
#    dict = json.load(blob_file)
#    json_json_str = json.dumps(dict)
    
    blob = bucket.get_blob(event['name'])
    data_json_str = blob.download_as_string()

    #data = file.read();
    #data_json = json.loads(data)


#    if data_json_str is None:
#        data_json_str = 'Data is empty'

    data_json = json.loads(data_json_str)

    sensor_name = data_json['sensorName']
    temperature = data_json['temperature']
    humidity = data_json['humidity']
    

    ###############################
    # move the data to Pubsub!

    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/pruebas-pubsub-systerminal/topics/topic-cf'

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
        publisher.publish(topic_path, data=message_bytes)
        #publish_future.result() # verify that the publish succeeded
    except Exception as e:
        print(e)
        return (e, 500)

    print('Message received from Bucket and published to Pubsub')

