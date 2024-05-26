from . import Api
from . import Operator
from . import MultiClusterHub
from time import sleep

class Acm(Operator):
    def __init__(self, api:Api) -> None:
        namespace = "open-cluster-management"
        super().__init__(api, "advanced-cluster-management", namespace)
        self.subscription.channel = "release-2.9"
        self.subscription.operator_group.spec["targetNamespaces"] = [namespace]
        self.hub = MultiClusterHub(self.api)

    def install(self) -> None:
        self.api.create_namespace_if_not_exist(self.namespace)
        super().install()
        # need to give time for new CRDs to be registered
        sleep(10)
        self.hub.install()

    def destroy(self) -> None:
        self.hub.destroy()
        super().destroy()
        self.api.destroy_namespace(self.namespace)
