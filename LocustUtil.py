import asyncio
import math
import os
import datetime
import random
import time
import json

import numpy as np
import paho.mqtt.client as mqtt


# map to count the number of user instance by type.
#from azure.eventhub import EventHubProducerClient, EventData

user_instance_map = {}


def get_id(self, prefix):
    """
    Returns the unique ID of running thread.
    :param self: FastHttpUser object
    :param prefix: prefix for ID
    :return: string representing unique ID (prefix + pod name + class name + locust thread number)
    """
    class_name = get_class_name(self)
    return get_id_from_type(self, prefix, class_name)


def get_id_from_type(self, prefix, device_type):
    """
    Returns the unique ID of running thread.
    :param self: FastHttpUser object
    :param prefix: prefix for ID
    :param device_type: device_Type (class name)
    :return: string representing unique ID (prefix + pod name + class name + locust thread number)
    """
    class_name = device_type
    thread_id = self._greenlet.getcurrent()
    instance_mum = 0

    if class_name in user_instance_map:
        thread_id_map = user_instance_map[class_name]
        if thread_id in thread_id_map:
            instance_num = thread_id_map[thread_id]
        else:
            instance_num = len(thread_id_map) + 1
            thread_id_map[thread_id] = instance_num
    else:
        thread_id_map = {thread_id: 1}
        user_instance_map[class_name] = thread_id_map
        instance_num = 1

    return "{}-{}-{}-{}".format(prefix, get_pod_name(), class_name, instance_num)


def get_class_name(self):
    '''
    Returns the class name.
    :param self:
    :return:
    '''
    return self.__class__.__name__


def get_current_timestamp():
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    return datetime.datetime.now(jst)


def get_current_time():
    """
    Returns current timestamp in Japan time in ISO 8601.
    :return: String (ex. 2020-08-25T12:10:31.908265+09:00)
    """
    return get_current_timestamp().isoformat()


def get_pod_name():
    """
    returns pod name that is set in environment variable of running container.
    :return:
    """
    return os.getenv("POD_NAME")


def get_access_token():
    """
    returns access token that is set in environment variable of running container.
    :return:
    """
    return os.getenv("ACCESS_TOKEN")


def wait_until_xth_second(second):
    """
    wait until xth second of every minute, where x is divisible by second in parameter.
    :param second: number to specify xth second. ex. 30 -> every 0 and 30th second of every minute.
                   60 -> every 0th second.
    """
    while True:
        if int(str(datetime.datetime.now())[17:19]) % second == 0:
            break
        else:
            time.sleep(0.2)
    return


def get_json_with_size(dict, n):
    """
    returns the json data with n byte.  If json is small, pad with dummy field.
    The resulting string may not be exactly n length, but approximately n length.
    :param dict:
    :param n:
    :return:
    """
    str = json.dumps(dict)
    if len(str) < n:
        dict["DUMMY_FIELD"] = "DUMMY" * ((n - len(str)) // 5)
    return json.dumps(dict)

def get_mqtt_username():
    '''
    returns the user name for MQTT connection.
    :return:
    '''
    return os.getenv("MQTT_USERNAME")

def get_mqtt_password():
    '''
    returns the password for MQTT connection.
    :return:
    '''
    return os.getenv("MQTT_PASSWORD")

def get_eventhubs_connection_string():
    '''
    returns the connection string for EVENT_HUBS connection.
    :return:
    '''
    return os.getenv("EVENTHUBS_CONNECTION_STRING")

def get_mqtt_endpoint():
    '''
    returns endpoint for MQTT connection.
    :return:
    '''
    return os.getenv("MQTT_ENDPOINT")


def get_mqtt_client():
    '''
    returns the instance of MQTT client
    :return:
    '''

    if "mqtt_client" in user_instance_map:
        return user_instance_map["mqtt_client"]
    else:
        mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
        mqtt_client.username_pw_set(get_mqtt_username(), get_mqtt_password())
        mqtt_client.tls_set(None, None, None)
        mqtt_client.tls_insecure_set(True)
        user_instance_map["mqtt_client"] = mqtt_client
        mqtt_client.connect(get_mqtt_endpoint(), 8883, keepalive=60)
        mqtt_client.loop_start()
        return mqtt_client
'''
    mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
    mqtt_client.username_pw_set(get_mqtt_username(), get_mqtt_password())
    mqtt_client.tls_set(None, None, None)
    mqtt_client.tls_insecure_set(True)
    user_instance_map["mqtt_client"] = mqtt_client
    mqtt_client.connect(get_mqtt_endpoint(), 8883, keepalive=60)
    mqtt_client.loop_start()
    return mqtt_client
'''

#        client.tls_set(CA_FILE_PATH,
#                       certfile='xxxxxxx.pem',
#                       keyfile='xxxxxxx.pem',
#                       tls_version=ssl.PROTOCOL_TLSv1_2)
#        client.tls_insecure_set(True)

'''
def publish_to_eventhubs(event_hub, data):

    map_key = 'amqp_messenger_' + event_hub
#    producer = user_instance_map[map_key] if map_key in user_instance_map \
#        else EventHubProducerClient.from_connection_string(conn_str=get_eventhubs_connection_string(), eventhub_name=event_hub)
    producer = EventHubProducerClient.from_connection_string(conn_str=get_eventhubs_connection_string(), eventhub_name=event_hub)

#    async def run():
#        async with producer:
#            # Create a batch.
#            event_data_batch = await producer.create_batch()

            # Add events to the batch.
#            event_data_batch.add(EventData(data))

            # Send the batch of events to the event hub.
#            await producer.send_batch(event_data_batch)

    # Create a batch.
    event_data_batch = producer.create_batch()

    # Add events to the batch.
    event_data_batch.add(EventData(data))

    # Send the batch of events to the event hub.
    producer.send_batch(event_data_batch)

#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(run())
#    run()
    producer.close()
    return
'''

class GenericSimulator:
    init_value = 0.0
    init_time = 0
    min = 0.0
    max = 0.0
    current = 0
    error_rate = 0.02  # error included in the simulated sensor value
    lambda_func = None
    message_seq = 0
    mttf = 0  # mean time to failure
    mttr = 0  # mean time to recovery
    next_failure_time = 0
    restart_time = 0
    next_restart_time = 0

    def __init__(self, init_value: float, _min: float, _max: float, error_rate: float, func):
        self.init_value = init_value
        self.init_time = time.time()
        self.min = _min
        self.max = _max
        self.error_rate = error_rate
        self.lambda_func = func

    def next_value(self):

        # simulate the broken device.
        if self.next_failure_time != 0 and self.next_failure_time < time.time():
            time.sleep(np.random.normal(self.mttr, self.mttr * 0.2, 1))
            self.set_failure_rate(self.mttf, self.mttr)

        # check whether to reset value.
        if self.next_restart_time != 0 and self.next_restart_time < time.time():
            self.current = self.init_value
            self.init_time = time.time()
            self.set_restart_time(self.restart_time)

        elapsed_time = time.time() - self.init_time
        self.current = self.lambda_func(elapsed_time, self.current)
        # apply min and max
        self.current = self.max if self.current > self.max else self.current
        self.current = self.min if self.current < self.min else self.current
        # add error
        self.current += np.random.randn() * self.error_rate * self.init_value

        # increment message sequence
        self.message_seq += 1

        return self.current

    def next_int(self):
        return int(self.next_value())

    def get_message_seq(self):
        return self.message_seq

    def set_failure_rate(self, mttf: int, mttr: int):
        '''
        set failure rate. if set, the device will stop after MTTF until MTTR is elapsed.
        :param mttf:  mean time to falire in seconds
        :param mttr:  mean time to recovery in seconds
        :return:
        '''
        self.next_failure_time = np.random.geometric(1.0 / mttf, 1) + time.time()
        self.mttf = mttf
        self.mttr = mttr

    def set_restart_time(self, restart_time: int):
        '''
        Set restart time. If the restart time has elapsed, then the current value is reset with initial value.
        example:  recharging the battery, etc.
        :param restart_time:
        :return:
        '''
        self.next_restart_time = restart_time + time.time()
        self.restart_time = restart_time


def get_simple_random_sensor_data(init_value, min, max, increment, error_rate):
    '''
    Generate random value based on the previous state and increment.
    example: temperature, wind, etc.
    :param init_value:
    :param min:
    :param max:
    :param increment:
    :param error_rate: error value (init_value * error_rate) is added to returned value
    :return:
    '''
    func = lambda elapsed_time, current: current + (random.random() - 0.5) * increment * 2
    return GenericSimulator(init_value, min, max, error_rate, func)


def get_cyclic_random_sensor_data(min: float, max: float, period: int, init_elapsed_time: int, error_rate: float):
    '''
    Generate random value based on the cycle.
    example: temperature, light, that fluctuates in a day etc.
    :type min: object
    :param period:  length of the cycle in seconds.  if period is 1 day, let it be (3600 * 24) seconds
    :param init_time: initial elapsed seconds.  if period is 1 day and init_time is 9:00 AM, then (3600 * 9) seconds
    :param min:
    :param max:
    :param error_rate:
    :return:
    '''
    func = lambda elapsed_time, current: \
        (math.sin((elapsed_time + init_elapsed_time) / period * 2 * math.pi) + 1) \
        / 2 * (max - min) + min
    return GenericSimulator((max + min) / 2, min, max, error_rate, func)


def get_diminishing_random_sensor_data(init_value: float, half_life_time: int, error_rate: float, restart_time: int):
    '''
    Generate random value based on
    :param init_value:
    :param half_life_time:
    :param error_rate:
    :param restart_time:
    :return:
    '''
    func = lambda elapsed_time, current: init_value * math.pow(0.5, elapsed_time / half_life_time)
    simulator = GenericSimulator(init_value, 0, init_value, error_rate, func)
    simulator.set_restart_time(restart_time)
    return simulator
