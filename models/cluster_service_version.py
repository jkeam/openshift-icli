from . import Api

class ClusterServiceVersion:
    def __init__(self) -> None:
        self.group = "operators.coreos.com"
        self.version = "v1alpha1"
        self.plural = "clusterserviceversions"
        self.kind = "ClusterServiceVersion"

    def destroy_all(self, api:Api, name:str):
        for m in self.find_matching(api, name):
            metadata = m["metadata"]
            name = metadata["name"]
            namespace = metadata["namespace"]
            api.destroy_dynamic_object(self.group, self.version, self.kind, name, namespace)

    def find_matching(self, api:Api, name:str) -> list[dict]:
        group = "operators.coreos.com"
        version = "v1alpha1"
        plural = "clusterserviceversions"

        csvs = (api.list_cluster_custom_object(group, version, plural))
        return list(filter(lambda c: name in c["metadata"]["name"], csvs["items"]))
