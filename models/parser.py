import yaml

class Parser:
    def __init__(self, filename:str="openshift-config.yaml") -> None:
        self.filename = filename

    def parse(self) -> dict:
        with open(self.filename, 'r') as file:
            config = yaml.safe_load(file)
            return config
