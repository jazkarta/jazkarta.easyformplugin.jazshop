import logging
import os

from collective.easyform.actions import Action, ActionFactory
from collective.easyform.api import get_context, get_expression
from plone.supermodel.exportimport import BaseHandler
from zope.interface import implementer

from . import _
from .interfaces import IJazShopCheckout

logger = logging.getLogger(__name__)


@implementer(IJazShopCheckout)
class JazShopCheckout(Action):
    """easyform action which .......... TODO
    """

    def __init__(self, **kw):
        for name, field in IJazShopCheckout.namesAndDescriptions():
            setattr(self, name, kw.pop(name, field.default))
        super(JazShopCheckout, self).__init__(**kw)

    def get_form(self):
        return get_context(self)

    def onSuccess(self, fields, request):
        """ TODO
        """
        form = self.get_form()
        # TODO



# Action factory used by the UI for adding a new easyform action
JazShopCheckoutAction = ActionFactory(
    JazShopCheckout,
    _(u"label_jazshopcheckout_action", default=u"Checkout with jazkarta.shop"),
    "jazkarta.easyformplugin.jazshop.AddJazShopCheckoutActions",
)


# Supermodel handler for serializing the action configuration to an XML model
JazShopCheckoutHandler = BaseHandler(JazShopCheckout)
