from . import Api

class KubeObject:
    def __init__(self) -> None:
        self.group = ""
        self.version = ""
        self.name = ""
        self.namespace = ""
        self.kind = ""
        self.spec = None

    def get_as_dict(self) -> dict[str, str|dict[str, str]]:
        obj:dict[str, str|dict[str, str]] = {
                "apiVersion": f"{self.group}/{self.version}",
                "kind": self.kind,
                "metadata": { "name": self.name, "namespace": self.namespace },
              }
        if self.spec is not None:
            obj["spec"] = self.spec

        return obj

    def wait_for_done(self, api:Api) -> None:
        if api is None:
            return
        api.watch(self.group, self.version, self.kind, self.namespace, self._ready)

    # Helpers
    def _ready(self, x:dict) -> bool:
        conditions = x.get("raw_object", {}).get("status", {}).get("conditions", [])
        if len(conditions) > 0:
            return conditions[0].get("type", "Not Ready") == "Ready"
        return False
