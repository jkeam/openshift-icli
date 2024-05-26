from . import Api
from . import KubeObject
from . import Serverless
from . import AmqStreams

class ServerlessEventingEventing(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "operator.knative.dev"
        self.version = "v1beta1"
        self.name = "knative-eventing"
        self.namespace = "knative-eventing"
        self.kind = "KnativeEventing"
        self.plural = "knative-eventings"
        self.spec = {
                "config": {
                    "default-ch-webhook": {
                        "default-ch-config": """clusterDefault:
  apiVersion: messaging.knative.dev/v1beta1
  kind: KafkaChannel
  spec:
    numPartitions: 1
    replicationFactor: 1 """
                        }
                    }
                }

    def destroy(self) -> None:
        body = self.get_as_dict()
        body["spec"] = {}

        existing = self.api.get_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.name)
        if existing is not None:
            self.api.create_or_replace_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, body)

class ServerlessEventingKafka(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "operator.serverless.openshift.io"
        self.version = "v1alpha1"
        self.name = "knative-kafka"
        self.namespace = "knative-eventing"
        self.kind = "KnativeKafka"
        self.spec = {
                "channel": {
                    "enabled": True,
                    "bootstrapServers": "my-cluster-kafka-bootstrap.kafka:9092"
                    },
                "source": {
                    "enabled": True
                    }
                }

class ServerlessEventing:
    def __init__(self, api:Api, validate_serverless:bool, validate_amqstreams:bool) -> None:
        self.api = api
        # not in openshift-config.yaml, need to check before install
        self.validate_serverless = validate_serverless
        self.validate_amqstreams = validate_amqstreams
        self.serverless_eventing_kafka = ServerlessEventingKafka(api)
        self.serverless_eventing_eventing = ServerlessEventingEventing(api)

    def install(self) -> None:
        # validate
        if self.validate_serverless:
            serverless = Serverless(self.api)
            eventing = serverless.eventing
            existing = self.api.get_namespaced_custom_object(eventing.group, eventing.version, eventing.namespace, f"{eventing.kind.lower()}s", eventing.name)
            if not existing:
                raise Exception("Serverless is a required prerequisite")

        if self.validate_amqstreams:
            amqstreams = AmqStreams(self.api)
            kafka = amqstreams.kafka
            existing = self.api.get_namespaced_custom_object(kafka.group, kafka.version, kafka.namespace, f"{kafka.kind.lower()}s", kafka.name)
            if not existing:
                raise Exception("AMQ Streams is a required prerequisite")

        self.serverless_eventing_kafka.install()
        self.serverless_eventing_eventing.install()

    def destroy(self) -> None:
        self.serverless_eventing_kafka.destroy()
        self.serverless_eventing_eventing.destroy()
