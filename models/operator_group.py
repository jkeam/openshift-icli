class OperatorGroup:
    def __init__(self, name:str, namespace:str) -> None:
        self.kind = "OperatorGroup"
        self.group = "operators.coreos.com"
        self.version = "v1"
        self.name = name
        self.namespace = namespace
        self.spec = {}

    def get_as_dict(self) -> dict:
        return {
                 "apiVersion": f"{self.group}/{self.version}",
                 "kind": self.kind,
                 "metadata": {"name": self.name, "namespace": self.namespace},
                 "spec": self.spec
               }
