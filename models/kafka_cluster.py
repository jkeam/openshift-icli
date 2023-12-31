from . import KubeObject
from . import Api

class KafkaCluster(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "kafka.strimzi.io"
        self.version = "v1beta2"
        self.name = "my-cluster"
        self.namespace = "kafka"
        self.kind = "Kafka"
        self.spec = {
                "kafka": {
                    "version": "3.5.0",
                    "replicas": 1,
                    "listeners": [{"name": "plain", "port": 9092, "type": "internal", "tls": False},
                                  {"name": "tls", "port": 9093, "type": "internal", "tls": True}],
                    "config": {
                        "offsets.topic.replication.factor": 1,
                        "transaction.state.log.replication.factor": 1,
                        "transaction.state.log.min.isr": 1,
                        "log.message.format.version": "3.5",
                        "inter.broker.protocol.version": "3.5"
                        },
                    "storage": {
                        "type": "jbod",
                        "volumes": [{"id": 0, "type": "persistent-claim", "size": "1Gi", "deleteClaim": False}]
                        }
                    },
                "zookeeper": {
                    "replicas": 1,
                    "storage": {
                        "type": "persistent-claim",
                        "size": "1Gi",
                        "deleteClaim": False
                        }
                    },
                "entityOperator": {
                    "topicOperator": {},
                    "userOperator": {}
                    }
                }
