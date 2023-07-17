from kubernetes import client, config, utils
from models import Serverless, Api, AmqStreams, Odf, Devspaces, ServerlessEventing
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

config.load_kube_config()

if __name__ == "__main__":
    api = Api(config, client, utils)
    serverless = Serverless(api)
    # serverless.install()
    # serverless.destroy()

    amq_streams = AmqStreams(api)
    # amq_streams.install()
    # amq_streams.destroy()

    serverless_eventing = ServerlessEventing(api)
    # serverless_eventing.install()
    # serverless_eventing.destroy()

    odf = Odf(api)
    # odf.install()
    # odf.destroy()

    devspaces = Devspaces(api)
    # devspaces.install()
    # devspaces.destroy()
