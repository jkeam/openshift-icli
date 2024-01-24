from . import Api, Operator, Keycloak

class Sso(Operator):
    def __init__(self, api:Api) -> None:
        self.namespace = "keycloak"
        super().__init__(api, "rhsso-operator", self.namespace)
        self.subscription.channel = "stable"
        self.subscription.operator_group.spec["targetNamespaces"] = [self.namespace]
        self.keycloak = Keycloak(self.api)
        self.keycloak.name = "sso"
        self.keycloak.namespace = self.namespace

    def install(self) -> None:
        self.api.create_namespace_if_not_exist(self.namespace)
        super().install()
        self.keycloak.install()

    def destroy(self) -> None:
        self.keycloak.destroy()
        super().destroy()
        self.api.destroy_namespace(self.namespace)
