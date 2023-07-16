from . import Api
from . import Subscription
from . import ClusterServiceVersion

class Odf:
    def __init__(self, api:Api):
        self.api = api
        namespace = "openshift-storage"
        self.subscription = Subscription(api, "odf-operator", namespace)
        self.subscription.channel = "stable-4.12"
        self.subscription.operator_group.spec["targetNamespaces"] = [namespace]

    def install(self):
        self.subscription.install()
        csv = ClusterServiceVersion()
        self.api.watch(csv.group, csv.version, csv.kind, self.subscription.namespace, self._install_done)

    def destroy(self):
        self.subscription.destroy()
        self.api.destroy_namespace(self.subscription.namespace)

    # Helpers
    def _install_done(self, x:dict) -> bool:
        return x.get("raw_object", {}).get("status", {}).get("phase", "Installing") == "Succeeded"
