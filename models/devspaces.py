from . import Api
from . import Subscription
from . import ClusterServiceVersion

class Devspaces:
    def __init__(self, api:Api):
        self.api = api
        self.subscription = Subscription(api, "devspaces", "openshift-devspaces")

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
