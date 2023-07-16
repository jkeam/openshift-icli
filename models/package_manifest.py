from . import Api

class PackageManifest:
    @staticmethod
    def find(api:Api, name:str, namespace:str="default"):
        pm = PackageManifest(api.get_namespaced_custom_object("packages.operators.coreos.com", "v1", namespace, "packagemanifests", name))
        return pm

    def __init__(self, data:dict) -> None:
        self.data = data

    def get_catalog_source(self) -> str:
        return self.data["status"]["catalogSource"]

    def get_catalog_source_namespace(self) -> str:
        return self.data["status"]["catalogSourceNamespace"]

    def get_name(self) -> str:
        return self.data["metadata"]["name"]

    def get_namespace(self) -> str:
        return self.data["metadata"]["namespace"]

    def get_stable_version(self) -> str:
        return self.get_csv_version("stable")

    def get_csv_version(self, name:str) -> str:
        channels = self.data["status"]["channels"]
        stable = ""
        for csv in list(map(lambda c: {"name": c["name"], "csv": c["currentCSV"]}, channels)):
            if csv["name"] == name:
                stable = csv["csv"]
        return stable
