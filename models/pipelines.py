from . import Api
from . import Operator

class Pipelines(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "openshift-pipelines-operator-rh")
        self.subscription.channel = "latest"
