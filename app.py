from kubernetes import client, config, utils
from models import Serverless, Api, AmqStreams
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

config.load_kube_config()

if __name__ == "__main__":
    api = Api(config, client, utils)
    serverless = Serverless(api)
    # serverless.install()
    # serverless.destroy()

    amq_streams = AmqStreams(api)
    amq_streams.install()
    # amq_streams.destroy()
