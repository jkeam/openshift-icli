from kubernetes import client, config, utils, watch
from openshift.dynamic import DynamicClient
from kubernetes.dynamic.exceptions import NotFoundError, ApiException
from time import sleep
from collections.abc import Callable

class Api:
    def __init__(self, config, client, utils):
        self.config = config
        self.client = client
        self.utils = utils
        self.custom_api = self.client.CustomObjectsApi()
        self.core_api = self.client.CoreV1Api()
        self.api_client = self.client.ApiClient()
        self.dyn_client = DynamicClient(config.new_client_from_config())

    # def get_custom_objects(self) -> list[dict]:
        # api = self.client.CustomObjectsApi()
        # ret = api.list_cluster_custom_object("packages.operators.coreos.com", "v1", "packagemanifests", pretty="false")
        # print(ret)

    # def get_cluster_custom_object(self, group:str, version:str, plural:str, name:str) -> CustomObject:
        # api = self.client.CustomObjectsApi()
        # return CustomObject(api.get_cluster_custom_object(group, version, plural, name))

    def watch(self, group:str, version:str, kind:str, namespace:str, stop_func:Callable[[dict], bool]):
        watcher = watch.Watch()
        func = self.dyn_client.resources.get(group=group, api_version=version, kind=kind)
        for e in func.watch(namespace=namespace, timeout=1200, watcher=watcher):
            sleep(5)
            if stop_func(e):
                watcher.stop()

    def list_cluster_custom_object(self, group:str, version:str, plural:str) -> list:
        return self.custom_api.list_cluster_custom_object(group, version, plural)

    def get_namespaced_custom_object(self, group:str, version:str, namespace: str, plural:str, name:str) -> dict|None:
        try:
            return self.custom_api.get_namespaced_custom_object(group, version, namespace, plural, name)
        except (NotFoundError, ApiException):
            return None

    def create_dynamic_object(self, group:str, version:str, kind:str, name:str, namespace:str, body:dict) -> None:
        api = self.dyn_client.resources.get(api_version=f"{group}/{version}", kind=kind)
        try:
            api.get(name=name, namespace=namespace)
        except NotFoundError:
            api.create(body=body, namespace=namespace)
            pass

    def create_or_replace_dynamic_object(self, group:str, version:str, kind:str, name:str, namespace:str, body:dict) -> None:
        api = self.dyn_client.resources.get(api_version=f"{group}/{version}", kind=kind)
        try:
            existing = api.get(name=name, namespace=namespace)
            body["metadata"]["resourceVersion"] = existing["metadata"]["resourceVersion"]
            api.replace(body=body, namespace=namespace)
        except NotFoundError:
            api.create(body=body, namespace=namespace)
            pass

    def destroy_dynamic_object(self, group:str, version:str, kind:str, name:str, namespace:str) -> None:
        api = self.dyn_client.resources.get(api_version=f"{group}/{version}", kind=kind)
        try:
            obj = api.get(name=name, namespace=namespace)
            if obj:
                api.delete(name=name, namespace=namespace)
        except NotFoundError:
            pass

    def create_namespace_if_not_exist(self, namespace:str) -> None:
        if not self._namespace_exists(namespace):
            namespace_config = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
            self.core_api.create_namespace(namespace_config)

    def destroy_namespace(self, namespace:str) -> None:
        if self._namespace_exists(namespace):
            self.core_api.delete_namespace(namespace)

    # Helpers
    def _get_namespaces(self) -> list:
        return self.core_api.list_namespace(pretty=False).items

    def _namespace_exists(self, namespace:str) -> bool:
        nms = self._get_namespaces()
        nms = list(map(lambda n: n.metadata.name, nms))
        return namespace in nms;
