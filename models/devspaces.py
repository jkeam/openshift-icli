from . import Api
from . import Operator

class Devspaces(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "devspaces", "openshift-devspaces")

    def destroy(self) -> None:
        super().destroy()
        self.api.destroy_namespace(self.subscription.namespace)
