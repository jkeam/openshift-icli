from . import OperatorGroup
from . import Api
from . import PackageManifest
from . import ClusterServiceVersion

class Subscription:
    def __init__(self, api:Api, name:str, namespace:str="openshift-operators") -> None:
        self.api = api
        self.group = "operators.coreos.com"
        self.version = "v1alpha1"
        self.kind = "Subscription"
        self.channel = "stable"
        self.install_plan_approval = "Automatic"
        self.name = name
        self.operator_name = name
        self.namespace = namespace
        self.catalog_source = "redhat-operators"
        self.catalog_source_namespace = "openshift-marketplace"
        self.operator_group = OperatorGroup(name, namespace)
        self.cluster_service_version = ""

    def get_as_dict(self) -> dict:
        return {
                "apiVersion": f"{self.group}/{self.version}",
                "kind": self.kind,
                "metadata": { "name": self.name, "namespace": self.namespace },
                "spec": {
                    "channel": self.channel,
                    "installPlanApproval": self.install_plan_approval,
                    "name": self.operator_name,
                    "source": self.catalog_source,
                    "sourceNamespace": self.catalog_source_namespace
                    }
                }

    def install(self) -> None:
        self.api.create_namespace_if_not_exist(self.namespace)

        package_manifest = PackageManifest.find(self.api, self.name)
        op = self.operator_group

        self.api.create_dynamic_object(op.group, op.version, op.kind, op.name, op.namespace, op.get_as_dict())
        self.api.create_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace, self.get_as_dict())

    def destroy(self) -> None:
        op = self.operator_group

        ClusterServiceVersion().destroy_all(self.api, self.name)
        self.api.destroy_dynamic_object(self.group, self.version, self.kind, self.name, self.namespace)
        self.api.destroy_dynamic_object(op.group, op.version, op.kind, op.name, op.namespace)
