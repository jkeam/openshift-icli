from . import Api
from . import ClusterServiceVersion
from . import Operator
from . import KubeObject

class ServerlessObject(KubeObject):
    def __init__(self) -> None:
        super().__init__()
        self.group = "operator.knative.dev"
        self.version = "v1beta1"

class ServerlessServing(ServerlessObject):
    def __init__(self) -> None:
        super().__init__()
        self.name = "knative-serving"
        self.namespace = "knative-serving"
        self.kind = "KnativeServing"

class ServerlessEventing(ServerlessObject):
    def __init__(self) -> None:
        super().__init__()
        self.name = "knative-eventing"
        self.namespace = "knative-eventing"
        self.kind = "KnativeEventing"

class Serverless(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "serverless-operator", "openshift-serverless")

    def install(self) -> None:
        super().install()
        self._install_serving()
        self._install_eventing()

    def destroy(self) -> None:
        eventing = ServerlessEventing()
        serving = ServerlessServing()
        self.api.destroy_namespace(eventing.namespace)
        self.api.destroy_namespace(serving.namespace)

        super().destroy()
        self.api.destroy_namespace(self.subscription.namespace)

    # Helpers
    def _install_serving(self) -> None:
        serving = ServerlessServing()
        self.api.create_namespace_if_not_exist(serving.namespace)
        self.api.create_dynamic_object(serving.group, serving.version, serving.kind, serving.name, serving.namespace, serving.get_as_dict())

    def _install_eventing(self) -> None:
        eventing = ServerlessEventing()
        self.api.create_namespace_if_not_exist(eventing.namespace)
        self.api.create_dynamic_object(eventing.group, eventing.version, eventing.kind, eventing.name, eventing.namespace, eventing.get_as_dict())
