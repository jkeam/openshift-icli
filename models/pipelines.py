from . import Api
from . import Operator

class Pipelines(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "openshift-pipelines-operator-rh", "openshift-pipelines")
        self.subscription.channel = "pipelines-1.11"

    def destroy(self) -> None:
        super().destroy()
        self.api.destroy_namespace(self.subscription.namespace)
