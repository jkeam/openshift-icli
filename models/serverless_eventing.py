from . import Api
from . import KubeObject

class ServerlessEventingEventing(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.ready_text = "InstallSucceeded"
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

    def install(self) -> None:
        self.api.create_or_replace_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())
        self.wait_for_done()

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
    def __init__(self, api:Api) -> None:
        self.api = api
        self.serverless_eventing_kafka = ServerlessEventingKafka(api)
        self.serverless_eventing_eventing = ServerlessEventingEventing(api)

    def install(self) -> None:
        self.serverless_eventing_kafka.install()
        self.serverless_eventing_eventing.install()

    def destroy(self) -> None:
        self.serverless_eventing_kafka.destroy()
        self.serverless_eventing_eventing.destroy()
