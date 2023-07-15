from . import Api
from . import Subscription
from . import ClusterServiceVersion

class ServerlessServing:
    def __init__(self):
        self.group = "operator.knative.dev"
        self.version = "v1beta1"
        self.name = "knative-serving"
        self.namespace = "knative-serving"
        self.kind = "KnativeServing"

    def get_as_dict(self) -> dict:
        return {
                 "apiVersion": f"{self.group}/{self.version}",
                 "kind": self.kind,
                 "metadata": { "name": self.name, "namespace": self.namespace }
               }

class ServerlessEventing:
    def __init__(self):
        self.group = "operator.knative.dev"
        self.version = "v1beta1"
        self.name = "knative-eventing"
        self.namespace = "knative-eventing"
        self.kind = "KnativeEventing"

    def get_as_dict(self) -> dict:
        return {
                 "apiVersion": f"{self.group}/{self.version}",
                 "kind": self.kind,
                 "metadata": { "name": self.name, "namespace": self.namespace }
               }

class Serverless:
    def __init__(self, api:Api):
        self.api = api
        self.subscription = Subscription(api, "serverless-operator", "openshift-serverless")

    def install(self):
        self.subscription.install()
        csv = ClusterServiceVersion()
        self.api.watch(csv.group, csv.version, csv.kind, self.subscription.namespace, self._install_done)
        self._install_serving()
        self._install_eventing()

    def destroy(self):
        eventing = ServerlessEventing()
        serving = ServerlessServing()
        self.api.destroy_namespace(eventing.namespace)
        self.api.destroy_namespace(serving.namespace)
        self.subscription.destroy()
        self.api.destroy_namespace(self.subscription.namespace)

    # Helpers
    def _install_done(self, x:dict) -> bool:
        return x.get("raw_object", {}).get("status", {}).get("phase", "Installing") == "Succeeded"

    def _install_serving(self):
        serving = ServerlessServing()
        self.api.create_namespace_if_not_exist(serving.namespace)
        self.api.create_dynamic_object(serving.group, serving.version, serving.kind, serving.name, serving.namespace, serving.get_as_dict())

    def _install_eventing(self):
        eventing = ServerlessEventing()
        self.api.create_namespace_if_not_exist(eventing.namespace)
        self.api.create_dynamic_object(eventing.group, eventing.version, eventing.kind, eventing.name, eventing.namespace, eventing.get_as_dict())
