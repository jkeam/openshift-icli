from kubernetes import client, config, utils
from models import Serverless, Api, AmqStreams, Odf, Devspaces, ServerlessEventing, Pipelines, Parser
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

config.load_kube_config()

def configure(debug: bool, api:Api, config:dict) -> (None|Devspaces|Pipelines|Odf|Serverless|AmqStreams|ServerlessEventing):
    name = config.get("name", "UNKNOWN")
    if name == "UNKNOWN":
        return None

    obj = None
    match name:
        case "devspaces" | "devspace" | "crw":
            obj = Devspaces(api)
        case "pipelines" | "pipeline" | "tekton":
            obj = Pipelines(api)
        case "odf" | "ocs" | "storage":
            obj = Odf(api)
        case "serverless" | "knative":
            obj = Serverless(api)
        case "amqstreams" | "kafka":
            obj = AmqStreams(api)
        case "serverless-eventing" | "knative-kafka":
            # TODO: Error check this.
            #   ServerlessEventing requires Serverless and AmqStreams to have been installed.
            obj = ServerlessEventing(api)
        case _:
            obj = None

    if obj is None:
        return obj

    if config.get("enabled", False):
        if debug:
            print(f"installing {name}")
        obj.install()
    else:
        if debug:
            print(f"uninstalling {name}")
        obj.destroy()
    return obj

if __name__ == "__main__":
    user_config = Parser().parse()
    spec = user_config.get("spec", {})
    debug = spec.get("debug", False)

    api = Api(config, client, utils)
    for operator in spec.get("operators", []):
        configure(debug, api, operator)
