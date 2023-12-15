from . import Api
from . import KubeObject

class MultiClusterHub(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.ready_text = "Complete"
        self.group = "operator.open-cluster-management.io"
        self.version = "v1"
        self.name = "multiclusterhub"
        self.namespace = "open-cluster-management"
        self.kind = "MultiClusterHub"
