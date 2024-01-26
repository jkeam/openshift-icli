from . import KubeObject
from . import Api

class CheCluster(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "org.eclipse.che"
        self.version = "v2"
        self.name = "devspaces"
        self.namespace = "openshift-devspaces"
        self.kind = "CheCluster"
        self.spec = {
                "components": {
                    "pluginRegistry": {
                        "openVSXURL": "https://open-vsx.org"
                    }
                },
                "containerRegistry": {},
                "devEnvironments": {},
                "gitServices": {},
                "networking": {}
                }

    def install(self) -> None:
        self.api.create_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())
        ready = lambda x: x.get("raw_object", {}).get("status", {}).get("chePhase", "NotReady") == "Active"
        self.api.watch(self.group, self.version, self.kind, self.namespace, ready)
