from kubernetes import client, config, utils
from models import Serverless, Api, AmqStreams, Odf, Devspaces, ServerlessEventing, Pipelines, Parser, ThreeScale, Camelk, Gitops, Acm, Sso
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

config.load_kube_config()

def configure(debug: bool, api:Api, config:dict, config_enabled_dict:dict[str:bool]) -> (None|Devspaces|Pipelines|Odf|Serverless|AmqStreams|ServerlessEventing):
    name = config.get("name", "UNKNOWN")
    if name == "UNKNOWN":
        return None

    obj = None
    match name:
        case "sso" | "keycloak":
            obj = Sso(api)
        case "acm":
            obj = Acm(api)
        case "argo" | "argocd" | "gitops":
            obj = Gitops(api)
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
            # check to see if serverless and amqstreams is in list
            serverless_enabled:bool = config_enabled_dict.get('serverless') or config_enabled_dict.get('knative')
            amqstreams_enabled:bool = config_enabled_dict.get('amqstreams') or config_enabled_dict.get('kafka')
            obj = ServerlessEventing(api, not serverless_enabled, not amqstreams_enabled)
        case "3scale" | "threescale" | "three-scale":
            obj = ThreeScale(api, config.get("spec", {}))
        case "camelk" | "camel-k":
            obj = Camelk(api)
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
    config_enabled_dict = dict(map(
        lambda x: (x.get("name", "UNKNOWN"), x.get("enabled", False)),
        spec.get("operators", [])
    ))
    for operator in spec.get("operators", []):
        configure(debug, api, operator, config_enabled_dict)
