from . import Api
from base64 import b64decode

class Secret:
    def __init__(self, api:Api, name:str, namespace:str, string_data:dict[str, str]) -> None:
        self.api = api
        self.name = name
        self.namespace = namespace
        self.string_data = string_data

    @classmethod
    def read(cls, api:Api, name:str, namespace:str):
        secret = api.get_secret(name, namespace, False)
        data = {}
        for key in secret.data:
            data[key] = b64decode(secret.data.get(key)).decode("ascii")
        return cls(api, name, namespace, data)

    def install(self) -> None:
        self.api.create_secret(self.name, self.namespace, self.string_data)

    def destroy(self) -> None:
        self.api.destroy_secret(self.name, self.namespace)
