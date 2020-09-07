from locust import task, between, TaskSet, events, User, LoadTestShape
import LocustUtil as Util

device_instance = {}  # keep the status of device instance


# The instance of HttpUser can represent one sensor/device.
class WindSensor(TaskSet):
    wait_time = between(1, 2)

    def on_start(self):
        self.parent.client = Util.get_mqtt_client()

    # instance of task can represent one type. (One device may send various data)
    @task
    def pub(self):

        # retrieve the dev instance
        dev_id = Util.get_id(self.parent, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_simple_random_sensor_data(init_value=20, min=0, max=50, increment=10, error_rate=0.1)
            device_instance[dev_id] = dev

        # create json data
        json_data = {
            "id": dev_id,
            "value": dev.next_int(),
            "seq": dev.get_message_seq(),
            "time": Util.get_current_time()
        }

        # send data to target
        rc, mid = self.parent.client.publish("/locust/mqtt/1",
                                             Util.get_json_with_size(json_data, 1000),
                                             qos=0, retain=True)

        if rc:
            events.request_failure.fire(
                request_type='publish',
                name=Util.get_class_name(self),
                response_time=0,
                exception=rc,
                response_length=1000
            )
        else:
            events.request_success.fire(
                request_type='publish',
                name=Util.get_class_name(self),
                response_time=0,
                response_length=1000,
            )
        return


# The instance of HttpUser can represent one sensor/device.
class TemperatureSensor(TaskSet):
    wait_time = between(1, 2)

    def on_start(self):
        self.parent.client = Util.get_mqtt_client()

    # instance of task can represent one type. (One device may send various data)
    @task
    def pub(self):

        # retrieve the dev instance
        dev_id = Util.get_id(self.parent, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_cyclic_random_sensor_data(init_elapsed_time=0, period=300, min=-10, max=45, error_rate=0.1)
            device_instance[dev_id] = dev

        # create json data
        json_data = {
            "id": dev_id,
            "value": dev.next_int(),
            "seq": dev.get_message_seq(),
            "time": Util.get_current_time()
        }

        # send data to target
        rc, mid = self.parent.client.publish("/locust/mqtt/1",
                                             Util.get_json_with_size(json_data, 1000),
                                             qos=0, retain=True)

        if rc:
            events.request_failure.fire(
                request_type='publish',
                name=Util.get_class_name(self),
                response_time=0,
                exception=rc,
                response_length=1000
            )
        else:
            events.request_success.fire(
                request_type='publish',
                name=Util.get_class_name(self),
                response_time=0,
                response_length=1000,
            )
        return


# The instance of HttpUser can represent one sensor/device.
class BatterySensor(TaskSet):
    wait_time = between(1, 2)

    def on_start(self):
        self.parent.client = Util.get_mqtt_client()

    # instance of task can represent one type. (One device may send various data)
    @task
    def pub(self):

        # retrieve the dev instance
        dev_id = Util.get_id(self.parent, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_diminishing_random_sensor_data(init_value=100, half_life_time=30, restart_time=120, error_rate=0.01)
            device_instance[dev_id] = dev

        # create json data
        json_data = {
            "id": dev_id,
            "value": dev.next_int(),
            "seq": dev.get_message_seq(),
            "time": Util.get_current_time()
        }

        # send data to target
        rc, mid = self.parent.client.publish("/locust/mqtt/1",
                                             Util.get_json_with_size(json_data, 1000),
                                             qos=0, retain=True)

        if rc:
            events.request_failure.fire(
                request_type='publish',
                name=Util.get_class_name(self),
                response_time=0,
                exception=rc,
                response_length=1000
            )
        else:
            events.request_success.fire(
                request_type='publish',
                name=Util.get_class_name(self),
                response_time=0,
                response_length=1000,
            )
        return


class Devices(User):
    tasks = [WindSensor, TemperatureSensor, BatterySensor]
    wait_time = between(1, 2)


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