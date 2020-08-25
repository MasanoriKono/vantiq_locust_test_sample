from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
import LocustUtil as Util


# token = qAwgPMF-dKZYt-jMlCY2-2Mv3nO3bCF3yT-rDt6PjeQ=
# URL = https://oheksfuji8.longnameofdomaintest.tk/
# path = /api/v1/resources/topics//locust/input
###
# env POD_NAME=DUMMY_POD ACCESS_TOKEN=qAwgPMF-dKZYt-jMlCY2-2Mv3nO3bCF3yT-rDt6PjeQ= locust -H
#     https://oheksfuji8.longnameofdomaintest.tk -f scenario-2.py --headless -u 20 -r 10

# The instance of HttpUser can represent one sensor/device.
class Device1(FastHttpUser):
    wait_time = between(1, 2)
    random1 = Util.RandomGen(init_value=200, lower_limit=100, higher_limit=300, change=10)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        # Send requests at Xth second of every minute.
        Util.wait_until_xth_second(20)

        json_data = {
            "id": Util.get_id(self, "dev"),   # "dev-xxxxx-n"
            "value": self.random1.next_int(),
            "Time": Util.get_current_time()
        }

        response = self.client.post(
            path="/api/v1/resources/topics//locust/input",
            data=Util.get_json_with_size(json_data, 1000),
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name="/locust/input"
        )

#        print(response.request.headers)
#        print("{}".format(json_data))


class Device2(FastHttpUser):
    wait_time = between(1, 2)
    random2 = Util.RandomGen(init_value=40, lower_limit=0, higher_limit=70, change=2)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        # Send requests at Xth second of every minute.
        Util.wait_until_xth_second(20)

        json_data = {
            "id": Util.get_id(self, "dev"),   # "dev-xxxxx-n"
            "value": self.random2.next_value(),
            "Time": Util.get_current_time()
        }

        response = self.client.post(
            path="/api/v1/resources/topics//locust/input",
            data=Util.get_json_with_size(json_data, 1000),
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name="/locust/input"
        )

#        print(response.request.headers)
#       print("{}".format(json_data))