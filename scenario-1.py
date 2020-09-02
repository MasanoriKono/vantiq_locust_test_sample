from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
import LocustUtil as Util


# The instance of HttpUser can represent one sensor/device.
class Device1(FastHttpUser):
    wait_time = between(1, 2)
    random1 = Util.get_simple_random_sensor_data(init_value=200, min=100, max=300, increment=10, error_rate=0.1)
    random1.set_failure_rate(20, 10)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        json_data = {
            "id": Util.get_id(self, "dev"),
            "value": self.random1.next_int(),
            "seq": self.random1.get_message_seq(),
            "Time": Util.get_current_time()
        }

        response = self.client.post(
            path="/api/v1/resources/topics//locust/input1",
            data=Util.get_json_with_size(json_data, 1000),
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name="/locust/input1"
        )


class Device2(FastHttpUser):
    wait_time = between(1, 2)
    random2 = Util.get_cyclic_random_sensor_data(init_elapsed_time=0, period=300, min=10, max=45, error_rate=0.1)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        json_data = {
            "id": Util.get_id(self, "dev"),
            "value": self.random2.next_value(),
            "seq": self.random2.get_message_seq(),
            "Time": Util.get_current_time()
        }

        response = self.client.post(
            path="/api/v1/resources/topics//locust/input2",
            data=Util.get_json_with_size(json_data, 1000),
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name="/locust/input2"
        )


class Device3(FastHttpUser):
    wait_time = between(1, 2)
    random3 = Util.get_diminishing_random_sensor_data(init_value=100, half_life_time=30, restart_time=120, error_rate=0.01)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        # Send requests at Xth second of every minute.
#        Util.wait_until_xth_second(10)

        message = {
            "id": Util.get_id(self, "dev"),   # "dev-xxxxx-n"
            "value": self.random3.next_value(),
            "seq": self.random3.get_message_seq(),
            "Time": Util.get_current_time()
        }
        json = Util.get_json_with_size(message, 1000)

        response = self.client.post(
            path="/api/v1/resources/topics//locust/input3",
            data=Util.get_json_with_size(message, 1000),
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name="/locust/input3"
        )

#        print(response.request.headers)
#       print("{}".format(json_data))