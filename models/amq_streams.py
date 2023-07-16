from . import Api
from . import Operator

class AmqStreams(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "amq-streams", "kafka")
