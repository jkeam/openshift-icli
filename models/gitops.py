from . import Api
from . import Operator
from . import Secret

class Gitops(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "openshift-gitops-operator", "openshift-gitops-operator")
        self.subscription.channel = "latest"

    def install(self) -> None:
        super().install()
        route = self.api.get_namespaced_custom_object("route.openshift.io", "v1", "openshift-gitops", "routes", "openshift-gitops-server").get("spec", {}).get("host", "")
        secret_seed = Secret.read(self.api, "openshift-gitops-cluster", "openshift-gitops")
        password = secret_seed.string_data.get("admin.password")
        print(f"\tusername: admin, password: {password}, url: https://{route}")

