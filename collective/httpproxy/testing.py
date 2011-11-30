from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.testing import z2


class HTTPProxyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.httpproxy
        self.loadZCML(package=collective.httpproxy)
        z2.installProduct(app, 'collective.httpproxy')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.httpproxy:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.httpproxy')

HTTP_PROXY_FIXTURE = HTTPProxyLayer()
HTTP_PROXY_INTEGRATION_TESTING = IntegrationTesting(bases=(HTTP_PROXY_FIXTURE, ),
                                                    name="HTTPProxy:Integration")
HTTP_PROXY_FUNCTIONAL_TESTING = FunctionalTesting(bases=(HTTP_PROXY_FIXTURE, ),
                                                  name="HTTPProxy:Functional")
