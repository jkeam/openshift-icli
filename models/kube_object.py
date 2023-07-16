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
