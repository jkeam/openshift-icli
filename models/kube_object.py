from . import Api

class KubeObject:
    def __init__(self, api:Api) -> None:
        self.group = ""
        self.version = ""
        self.name = ""
        self.namespace = ""
        self.kind = ""
        self.spec = None
        self.api = api
        self.ready_text = "Ready"

    def get_as_dict(self) -> dict[str, str|dict[str, str]]:
        obj:dict[str, str|dict[str, str]] = {
                "apiVersion": f"{self.group}/{self.version}",
                "kind": self.kind,
                "metadata": { "name": self.name, "namespace": self.namespace },
              }
        if self.spec is not None:
            obj["spec"] = self.spec

        return obj

    def install(self) -> None:
        self.api.create_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())
        self.wait_for_done()

    def destroy(self):
        self.api.destroy_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace)

    def wait_for_done(self) -> None:
        if self.api is None:
            return
        self.api.watch(self.group, self.version, self.kind, self.namespace, self._ready)

    # Helpers
    def _ready(self, x:dict) -> bool:
        conditions = x.get("raw_object", {}).get("status", {}).get("conditions", [])
        if len(conditions) > 0:
            datetime = conditions[0].get("lastTransitionTime", "")
            last_conditions = list(filter(lambda c: c.get("lastTransitionTime", "") == datetime, conditions))
            last_types = list(map(lambda c: c.get("type", "NotReady"), last_conditions))
            return self.ready_text in last_types
        return False
