from kubernetes import client, config, utils
from openshift.dynamic import DynamicClient
from kubernetes.dynamic.exceptions import NotFoundError
from models import Subscription
from models import Api

config.load_kube_config()

if __name__ == "__main__":
    api = Api(config, client, utils)
    subscription = Subscription(api, "serverless-operator", "openshift-serverless")
    # subscription.install()
    # subscription.destroy()
