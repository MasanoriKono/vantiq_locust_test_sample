# Locust Test for VANTIQ
This project is the template for writing the load test using locust.

# Get Started

### Run from local machine

- clone the project in the local.
```bash
git clone https://github.com/MasanoriKono/vantiq_locust_test_sample.git
```

- import the folder `resources/locusttest` as VANTIQ project In VANTIQ IDE. 
- import the data `resource/data/SensorDetails.json` as data in VANTIQ IDE.
- generate VANTIQ access token from the namespace.
- install the dependencies
```shell script
pip3 install -r requirements.txt
```
- in the project root folder, run the command:
```shell script
env POD_NAME=local-run \
ACCESS_TOKEN=<access token> \
locust -H https://<vantiq host> -f scenario-XX.py --headless
```

- run this command for MQTT broker scenario:
```shell script
env POD_NAME=local-run \
MQTT_USERNAME=<mqtt_username> \
MQTT_PASSWORD=<mqtt_password> \
MQTT_ENDPOINT=<mqtt_endpoint> \
locust -H https://<vantiq host> -f scenario-14.py --headless
```

- run this command for Azure Eventhubs broker scenario:
```shell script
env POD_NAME=local-run \
EVENTHUBS_CONNECTION_STRING=<eventhubs_connection_string> \
locust -H https://<vantiq host> -f scenario-16.py --headless
```

- remove `--headless` to use the web UI to start / stop the test:
```shell script
env POD_NAME=local-run \
ACCESS_TOKEN=<access token> \
locust -H https://<vantiq host> -f scenario-XX.py 
```

- remove `CustomLoadTestShape` class to apply the parameter from command line
```shell script
env POD_NAME=local-run \
ACCESS_TOKEN=<access token> \
locust -H https://<vantiq host> -f scenario-XX.py --headless -u 20 -r 10
```

### Run from kubenetes cluster

- clone the project in the local.
```bash
git clone https://github.com/MasanoriKono/vantiq_locust_test_sample.git
```
- check the project into your own github account. 
- import the folder `resources/locusttest` as VANTIQ project In VANTIQ IDE. 
- import the data `resource/data/SensorDetails.json` as data in VANTIQ IDE.
- get VANTIQ access token from the namespace.
- udpate config in `k8s/LocustConfigMap.yanl`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: locust-param
data:
  VANTIQ_HOST: "<vantiq_host>"
  ACCESS_TOKEN: "<access_token>"
  GITHUB_REPO_URL: "<your github repository>"
  SCENARIO: "scenario-XX.py"
  MQTT_USERNAME: "<mqtt_username>"
  MQTT_PASSWORD: "<mqtt_password>"
  MQTT_ENDPOINT: "<mqtt_endpoint>"
  EVENTHUBS_CONNECTION_STRING : "<eventhubs_connection_string>"
  TEST_VERSION: "3"
```
- configure `spec.replicas` parameter in `k8s/LocustSTS.yaml` for the cluster size:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: locust
spec:
  selector:
    matchLabels:
      app: locust
  serviceName: "locust"
  replicas: 5
  template:
    metadata:
      labels:
        app: locust
```
- deploy the test driver to kubernetes cluster
```shell script
kubectl apply -f k8s/
```
- connect to locust web via port-forward
```shell script
kubectl port-forward locust-0 30089:8089
open http://localhost:30089
```
- to change the scenario, update `k8s/LocustConfigMap.yaml` and run the command:
```shell script
kubectl delete -f k8s/
kubectl apply -f k8s/
```

### sample scenarios

1. type - insert + delete
1. type - upsert
1. stateless - transform
1. stateless - filter
1. stateful - smooth
1. stateful - sample
1. stateful - limit
1. stateful - delay
1. split by group - dwell
1. split by group - join
1. split by group - missing
1. split by group - cached_enrich
1. split by group - enrich (type select)
1. ingest - mqtt
1. ingest - amqp (azure eventhub - only works in local)
1. ingest - kafka (not implemented yet)
1. ingest - https rest
1. load pattern - uniformly distributed load
1. load pattern - spike 


## Reference

- [Locust](https://github.com/locustio/locust)
