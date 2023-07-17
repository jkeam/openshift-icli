from . import Api
from . import Operator
from . import KubeObject

class ServerlessObject(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "operator.knative.dev"
        self.version = "v1beta1"

class ServerlessServing(ServerlessObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.name = "knative-serving"
        self.namespace = "knative-serving"
        self.kind = "KnativeServing"

class ServerlessEventing(ServerlessObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.name = "knative-eventing"
        self.namespace = "knative-eventing"
        self.kind = "KnativeEventing"

class Serverless(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "serverless-operator", "openshift-serverless")
        self.serving = ServerlessServing(self.api)
        self.eventing = ServerlessEventing(self.api)

    def install(self) -> None:
        super().install()
        self.api.create_namespace_if_not_exist(self.serving.namespace)
        self.serving.install()
        self.api.create_namespace_if_not_exist(self.eventing.namespace)
        self.eventing.install()

    def destroy(self) -> None:
        self.serving.destroy()
        self.eventing.destroy()
        self.api.destroy_namespace(self.serving.namespace)
        self.api.destroy_namespace(self.eventing.namespace)

        super().destroy()
        self.api.destroy_namespace(self.subscription.namespace)
