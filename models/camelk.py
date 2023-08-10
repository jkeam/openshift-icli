from . import Api
from . import Operator

class Camelk(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "red-hat-camel-k")
        self.subscription.channel = "latest"
