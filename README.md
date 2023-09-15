# OpenShift Interactive CLI

Use this to install things like Operators from the CLI.
The idea is that you can create an `openshift-config.yaml`,
and then run this tool and all of the operators you specified
will be installed.

Here is a simple example of the config:

```yaml
apiVersion: openshift.keam.io/v1alpha1
kind: OpenshiftConfig
spec:
  debug: true
  operators:
    - name: devspaces
      enabled: true
    - name: pipelines
      enabled: true
    - name: odf
      enabled: true
    - name: serverless
      enabled: true
    - name: amqstreams
      enabled: true
    - name: serverless-eventing
      enabled: true
    - name: camel-k
      enabled: true
    - name: threescale
      enabled: true
```

## Prerequisite

1. Python 3.x
2. OpenShift 4.x

## Running

Ensure you are logged into OpenShift first.

```shell
python3.11 -m venv venv
source ./venv/bin/activate
pip install -r ./requirements.txt
python ./app.py
```
