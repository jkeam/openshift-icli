from . import Api
from . import Operator
from . import CheCluster
from time import sleep

class Devspaces(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "devspaces", "openshift-devspaces")
        self.che_cluster = CheCluster(self.api)

    def install(self) -> None:
        super().install()
        # need to give time for new CRDs to be registered
        sleep(10)
        self.che_cluster.install()

    def destroy(self) -> None:
        self.che_cluster.destroy()
        super().destroy()
        self.api.destroy_namespace(self.subscription.namespace)
