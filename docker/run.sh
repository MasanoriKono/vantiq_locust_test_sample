#!/bin/bash
git clone $GITHUB_REPO_URL
cd $(ls -d */ | head -n 1)
pip3 install -r requirements.txt
if [[ "$POD_NAME" == "locust-0" ]] ; then
  locust -H $VANTIQ_HOST -f $SCENARIO --master
elif [[ "$POD_NAME" =~ ^locust-[0-9]+ ]] ; then
  locust -H $VANTIQ_HOST -f $SCENARIO --worker --master-host locust-0.locust.default.svc.cluster.local
else
  locust -H $VANTIQ_HOST -f $SCENARIO
fi
