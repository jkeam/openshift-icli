from . import Api, KubeObject

class QuayRegistry(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "quay.redhat.com"
        self.version = "v1"
        self.name = "quay-registry"
        self.namespace = "quay-enterprise"
        self.kind = "QuayRegistry"
        self.ready_text = "Available"
        self.secretname = "config-bundle-secret"
        self.spec = {
            "configBundleSecret": self.secretname,
            "components": [{
                "kind": "objectstorage",
                "managed": False
            }]
        }

    def _ready(self, x:dict) -> bool:
        conditions = x.get("raw_object", {}).get("status", {}).get("conditions", [])
        if len(conditions) > 0:
            for c in conditions:
                if c.get("type") == self.ready_text:
                    return c.get("status") == "True"
        return False
            
    def install(self) -> None:
        self.api.create_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())
        self.api.watch(self.group, self.version, self.kind, self.namespace, self._ready)
