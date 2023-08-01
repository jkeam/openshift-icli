from kubernetes.dynamic.exceptions import ResourceNotFoundError
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
        self.api.create_or_replace_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())
        self.wait_for_done()

    def destroy(self):
        try:
            self.api.destroy_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace)
        except ResourceNotFoundError:
            pass

    def wait_for_done(self) -> None:
        if self.api is None:
            return
        self.api.watch(self.group, self.version, self.kind, self.namespace, self._ready)

    # Helpers
    def _ready(self, x:dict) -> bool:
        conditions = x.get("raw_object", {}).get("status", {}).get("conditions", [])
        if len(conditions) > 0:
            sort_field = "lastTransitionTime"
            sorter = lambda x: x[sort_field]
            conditions.sort(reverse=True, key=sorter)
            datetime = conditions[0].get(sort_field, "")
            last_conditions = list(filter(lambda c: c.get(sort_field, "") == datetime, conditions))
            last_types = list(map(lambda c: c.get("type", "NotReady"), last_conditions))
            return self.ready_text in last_types
        return False
