from . import Api
from . import Operator
from . import KafkaCluster

class AmqStreams(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "amq-streams", "kafka")

    def install(self) -> None:
        super().install()
        kafka = KafkaCluster()
        self.api.create_dynamic_object(kafka.group, kafka.version, kafka.kind, kafka.name, kafka.namespace, kafka.get_as_dict())
        kafka.wait_for_done(self.api)

    def destroy(self) -> None:
        super().destroy()
