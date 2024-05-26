from . import Api, KubeObject

class Keycloak(KubeObject):
    def __init__(self, api:Api) -> None:
        super().__init__(api)
        self.group = "keycloak.org"
        self.version = "v1alpha1"
        self.name = "sso"
        self.namespace = "keycloak"
        self.kind = "Keycloak"
        self.spec = {
            "instances": 1,
            "externalAccess": {
                "enabled": True
            },
            "externalDatabase": {
                "enabled": False
            },
            "postgresDeploymentSpec": {
                "imagePullPolicy": "Always"
            },
            "keycloakDeploymentSpec": {
                "imagePullPolicy": "Always",
                "experimental": {
                    "env": [{
                        "name": "JAVA_TOOL_OPTIONS",
                        "value": "-Dcom.redhat.fips=false"
                    }]
                }
            }
        }

    def ready(self, x):
        is_ready = x.get("raw_object", {}).get("status", {}).get("ready", "false")
        return is_ready == "true" or is_ready

    def install(self) -> None:
        self.api.create_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())
        self.api.watch(self.group, self.version, self.kind, self.namespace, self.ready)
