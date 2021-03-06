from locust import task, between, SequentialTaskSet, LoadTestShape
from locust.contrib.fasthttp import FastHttpUser
import LocustUtil as Util

device_instance = {}  # keep the status of device instance


# The instance of HttpUser can represent one sensor/device.
class Device1(FastHttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # retrieve the dev instance
        dev_id = Util.get_id(self, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_simple_random_sensor_data(init_value=200, min=100, max=300, increment=10, error_rate=0.1)
            dev.set_failure_rate(20, 10)
            device_instance[dev_id] = dev


    @task
    class InsertDeleteSequence(SequentialTaskSet):

        # instance of task can represent one type. (One device may send various data)
        @task
        def insert(self):

            dev_id = Util.get_id(self.parent, "dev")
            dev = device_instance[dev_id]

            # create json data
            json_data = {
                "id": dev_id,
                "value": dev.next_int(),
                "seq": dev.get_message_seq(),
                "op" : "INSERT",
                "Time": Util.get_current_time()
            }

            # send data to target
            response = self.client.post(
                path="/api/v1/resources/topics//locust/input1",
                data=Util.get_json_with_size(json_data, 1000),
                auth=None,
                headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                         "Content-Type": "application/json"},
                name=Util.get_class_name(self)
            )

        @task
        def delete(self):

            dev_id = Util.get_id(self.parent, "dev")
            dev = device_instance[dev_id]

            # create json data
            json_data = {
                "id": dev_id,
                "value": dev.next_int(),
                "seq": dev.get_message_seq(),
                "op" : "DELETE",
                "Time": Util.get_current_time()
            }

            # send data to target
            response = self.client.post(
                path="/api/v1/resources/topics//locust/input1",
                data=Util.get_json_with_size(json_data, 1000),
                auth=None,
                headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                         "Content-Type": "application/json"},
                name=Util.get_class_name(self)
            )


class CustomLoadTestShape(LoadTestShape):
    time_limit = 3600
    spawn_rate = 20
    start_user = 1000
    stage_increment = 1000
    stage_duration = 300
    cool_down_duration = 60

    def tick(self):

        run_time = self.get_run_time()

        cycle = int(run_time) // (self.stage_duration + self.cool_down_duration)

        if run_time % (self.stage_duration + self.cool_down_duration) < self.stage_duration:
            user_count = self.start_user + cycle * self.stage_increment
        else:
            user_count = 0

        return user_count, self.spawn_rate