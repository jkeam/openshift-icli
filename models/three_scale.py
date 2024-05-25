from . import Api
from . import Operator
from . import KubeObject
from . import Secret

class ThreeScaleApiManager(KubeObject):
    def __init__(self, api:Api, name:str, namespace:str, wildcard_domain:str, secret_name:str) -> None:
        super().__init__(api)
        self.wildcard_domain = wildcard_domain
        self.secret_name = secret_name

        self.ready_text = "Available"
        self.group = "apps.3scale.net"
        self.version = "v1alpha1"
        self.name = name
        self.namespace = namespace
        self.kind = "APIManager"
        self.plural = "apimanagers"
        self.spec = {
                "wildcardDomain": wildcard_domain,
                "system": {
                    "fileStorage": {
                        "simpleStorageService": {
                            "configurationSecretRef": {
                                "name": secret_name
                                }
                            }
                        }
                    }
                }

class ThreeScaleApicast(Operator):
    def __init__(self, api:Api) -> None:
        super().__init__(api, "apicast-operator", "3scale-project", True)
        self.subscription.channel = "threescale-2.13"

class ThreeScale(Operator):
    def __init__(self, api:Api, config:dict) -> None:
        self.namespace = "3scale-project"
        super().__init__(api, "3scale-operator", self.namespace)
        self.subscription.channel = "threescale-2.13"
        self.apicast = ThreeScaleApicast(api)

        aws_config:dict[str, str] = config.get("aws", {})
        secret_data = {
                "AWS_ACCESS_KEY_ID": aws_config.get("access_key_id", ""),
                "AWS_SECRET_ACCESS_KEY": aws_config.get("access_key_secret", ""),
                "AWS_BUCKET": aws_config.get("bucket_name", ""),
                "AWS_REGION": aws_config.get("region", "")
                }
        self.secret = Secret(api, "aws-auth", self.namespace, secret_data)
        self.api_manager = ThreeScaleApiManager(api, "apimanager", self.namespace, config.get("wildcard_domain", ""), self.secret.name)

    def install(self) -> None:
        super().install()
        self.apicast.install()
        self.secret.install()
        # FIXME: polling condition for apicast prematurely exists and api manager is attempted to be installed before ready
        self.api_manager.install()
        secret_seed = Secret.read(self.api, "system-seed", self.namespace)
        admin_username = secret_seed.string_data.get("ADMIN_USER")
        admin_password = secret_seed.string_data.get("ADMIN_PASSWORD")
        print(f"\tusername: {admin_username}, password: {admin_password}, url: https://3scale-admin.{self.api_manager.wildcard_domain}")

    def destroy(self) -> None:
        self.api_manager.destroy()
        self.secret.destroy()
        self.apicast.destroy()
        super().destroy()
