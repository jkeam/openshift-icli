from . import Api
from . import Operator
from . import KafkaCluster
from time import sleep

class AmqStreams(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "amq-streams", "amq-streams-kafka")
        self.kafka = KafkaCluster(self.api)

    def install(self) -> None:
        self.api.create_namespace_if_not_exist(self.namespace)
        super().install()
        # need to give time for new CRDs to be registered
        sleep(10)
        self.api.create_namespace_if_not_exist(self.kafka.namespace)
        self.kafka.install()

    def destroy(self) -> None:
        self.kafka.destroy()
        super().destroy()
        self.api.destroy_namespace(self.kafka.namespace)
        self.api.destroy_namespace(self.namespace)
