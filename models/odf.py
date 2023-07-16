from . import Api
from . import Operator

class Odf(Operator):
    def __init__(self, api:Api) -> None:
        namespace = "openshift-storage"
        super().__init__(api, "odf-operator", namespace)
        self.subscription.channel = "stable-4.12"
        self.subscription.operator_group.spec["targetNamespaces"] = [namespace]

    def destroy(self) -> None:
        super().destroy()
        self.api.destroy_namespace(self.subscription.namespace)
