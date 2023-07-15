from . import Api
from . import Subscription

class Serverless:
    def __init__(self, api:Api):
        self.subscription = Subscription(api, "serverless-operator", "openshift-serverless")

    def install(self):
        self.subscription.install()

    def destroy(self):
        self.subscription.destroy()
