from . import Api
from . import Operator
from . import KafkaCluster

class AmqStreams(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "amq-streams", "kafka")
        self.kafka = KafkaCluster(self.api)

    def install(self) -> None:
        super().install()
        self.kafka.install()

    def destroy(self) -> None:
        self.kafka.destroy()
        super().destroy()
