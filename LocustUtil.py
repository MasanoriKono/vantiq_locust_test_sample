import os
import random
import datetime
import time
import json

# map to count the number of user instance by type.
user_instance_map = {}

def get_id(self, prefix):
    """
    Returns the unique ID of running thread.
    :param self: FastHttpUser object
    :param prefix: prefix for ID
    :return: string representing unique ID (prefix + pod name + class name + locust thread number)
    """
    class_name = self.__class__.__name__
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


def get_current_time():
    """
    Returns current timestamp in Japan time in ISO 8601.
    :return: String (ex. 2020-08-25T12:10:31.908265+09:00)
    """
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    return datetime.datetime.now(jst).isoformat()


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


class RandomGen:

    init_value = 0
    lower_limit = 0
    higher_limit = 0
    change = 0
    current_value = 0

    def __init__(self, init_value, lower_limit, higher_limit, change):
        self.init_value = init_value
        self.lower_limit = lower_limit
        self.higher_limit = higher_limit
        self.change = change
        self.current_value = init_value

    def next_value(self):
        self.current_value += (random.random() - 0.5) * self.change * 2
        return self.current_value

    def next_int(self):
        return int(self.next_value())
