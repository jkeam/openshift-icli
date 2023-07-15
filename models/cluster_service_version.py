from . import Api

class ClusterServiceVersion:
    @staticmethod
    def destroy_all(api:Api, name:str):
        group = "operators.coreos.com"
        version = "v1alpha1"
        plural = "clusterserviceversions"

        csvs = (api.list_cluster_custom_object(group, version, plural))
        matching = list(filter(lambda c: name in c["metadata"]["name"], csvs["items"]))
        for m in matching:
            metadata = m["metadata"]
            name = metadata["name"]
            namespace = metadata["namespace"]
            api.destroy_dynamic_object(group, version, "ClusterServiceVersion", name, namespace)
