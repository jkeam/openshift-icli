from . import Api
from . import Subscription
from . import ClusterServiceVersion

class Operator:
    def __init__(self, api:Api, name:str, namespace:str="openshift-operators") -> None:
        self.api = api
        self.name = name
        self.namespace = namespace
        self.subscription = Subscription(api, name, namespace)

    def install(self) -> None:
        self.subscription.install()
        csv = ClusterServiceVersion()
        self.api.watch(csv.group, csv.version, csv.kind, self.subscription.namespace, self._install_done)

    def destroy(self) -> None:
        self.subscription.destroy()
        if "openshift" not in self.namespace:
            self.api.destroy_namespace(self.subscription.namespace)

    # Helpers
    def _install_done(self, x:dict) -> bool:
        return x.get("raw_object", {}).get("status", {}).get("phase", "Installing") == "Succeeded"
