from . import Api, Operator, QuayRegistry, Secret
from json import dumps

class Quay(Operator):
    def __init__(self, api:Api, config:dict) -> None:
        self.namespace = "quay-enterprise"
        super().__init__(api, "quay-operator", self.namespace)
        self.subscription.channel = "stable-3.10"
        self.registry = QuayRegistry(self.api)
        self.registry.name = "quay-registry"
        self.registry.namespace = self.namespace
        self.registry.secretname = "config-bundle-secret"
        aws_config:dict[str, str] = config.get("aws", {})
        secret_data_value = {
            "DISTRIBUTED_STORAGE_CONFIG": {
                "s3Storage": [
                    "S3Storage",
                    {
                        "host": f"s3.{aws_config.get('region', '')}.amazonaws.com",
                        "s3_access_key": aws_config.get("access_key_id", ""),
                        "s3_secret_key": aws_config.get("access_key_secret", ""),
                        "s3_bucket": aws_config.get("bucket_name", ""),
                        "storage_path": "/datastorage/registry"
                    }
                ]
            },
            "DISTRIBUTED_STORAGE_DEFAULT_LOCATIONS": [],
            "DISTRIBUTED_STORAGE_PREFERENCE": ["s3Storage"]
        }
        self.secret = Secret(api, self.registry.secretname, self.namespace, {"config.yaml": dumps(secret_data_value)})

    def install(self) -> None:
        self.api.create_namespace_if_not_exist(self.namespace)
        super().install()
        self.secret.install()
        self.registry.install()

    def destroy(self) -> None:
        self.registry.destroy()
        self.secret.destroy()
        super().destroy()
        self.api.destroy_namespace(self.namespace)
