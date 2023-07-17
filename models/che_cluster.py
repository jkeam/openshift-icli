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
                "components": {},
                "containerRegistry": {},
                "devEnvironments": {},
                "gitServices": {},
                "networking": {}
                }
