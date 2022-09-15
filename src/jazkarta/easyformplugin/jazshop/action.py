import logging
import os
from decimal import Decimal
from collective.easyform.actions import Action, ActionFactory
from collective.easyform.api import get_context, get_expression
from plone.supermodel.exportimport import BaseHandler
from zope.interface import implementer
from zope.interface import directlyProvides
from zope.interface import implements
from jazkarta.shop.cart import Cart
from Products.statusmessages.interfaces import IStatusMessage

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

    def _get_item_details(self, pfg_form, REQUEST):
        # XXX Test this, see whats required and what is not
        pass
        """
        details = '<p></p><h2>{}</h2><dl>'.format(pfg_form.title)
        form_fields = {}
        fields = pfg_form._getFieldObjects()
        for field in fields:
            label = field.fgField.widget.label
            value = field.htmlValue(REQUEST)
            form_fields[field.id] = value
            details += '<dt>{}</dt><dd>{}</dd>'.format(label, value)
        details += '</dl><p></p>'
        return form_fields, details
        """

    def onSuccess(self, fields, request):
        """ TODO
        """
        form = self.get_form()
        print "SUCCESSFULL ACTION EXECUTED"
        # TODO


        # XXX Test this, see whats required and what is not
        """
        item_prepend = None
        if getattr(self, 'formIdExpression', None):
            try:
                item_prepend = self.formIdExpression.format(**REQUEST.form)
            except (KeyError, ValueError):
                pass
        cart = Cart.from_request(REQUEST)
        products = []
        pfg_products = []
        arbitrary = []
        if 'pfg_products' not in cart.data:
            cart.data['pfg_products'] = {}
        if 'pfg_details' not in cart.data:
            cart.data['pfg_details'] = {}
        if 'pfg_forms' not in cart.data:
            cart.data['pfg_forms'] = {}
        for field in fields:
            if field.portal_type in JAZSHOP_FIELDS:
                value = REQUEST.form.get(field.id)
                if not value:
                    continue
                if isinstance(value, list):
                    value = map(lambda x: x.split('|')[-1], value)
                    products.extend(value)
                else:
                    value = value.split('|')[-1]
                    products.append(value)
            if field.portal_type == 'JazShopArbitraryPriceStringField':
                price = REQUEST.form.get(field.id)
                if not price or not field.availableProducts:
                    continue
                product_value = field.availableProducts[0]
                product_uid = product_value.split('|')[-1]
                cart.add_product(product_uid)
                arbitrary.append(product_uid)
                for item in cart._items.values():
                    if item['uid'] == product_uid:
                        price = price.replace('$', '')
                        item['price'] = Decimal(price)
        for uid in products:
            if uid != '0':
                cart.add_product(uid)
                pfg_products.append(uid)
        if item_prepend is not None:
            for item in cart._items.values():
                if (item['uid'] in (products + arbitrary) and
                        not item['name'].startswith(item_prepend)):
                    item['name'] = item_prepend + item['name']
        # store form fields and reference to this form
        pfg_form = self.aq_parent
        pfg_form_uid = self.aq_parent.UID()
        cart.data['pfg_products'][pfg_form_uid] = pfg_products
        fields, details = self._get_item_details(pfg_form, REQUEST)
        cart.data['pfg_forms'][pfg_form_uid] = fields
        cart.data['pfg_details'][pfg_form_uid] = details
        order_details = ''
        cart_products = [i.uid for i in cart.items]
        for form_uid in cart.data['pfg_forms'].keys():
            form_products = cart.data['pfg_products'][form_uid]
            in_cart = True
            for p in form_products:
                if p not in cart_products:
                    in_cart = False
            if in_cart:
                order_details += cart.data['pfg_details'][form_uid]
        cart.data['order_details'] = order_details
        cart.save()


        def get_selected_products(context, value):
            selected = []
            products = context.portal_catalog(
                object_provides=IProduct.__identifier__,
                sort_on='sortable_title',
                sort_order='ascending')
            product_dict = {product.UID: ("{}|{}".format(product.Title, product.UID), "$" + str(product.getObject().price) + ' - ' + product.Title) for product in products}
            for product in value:
                if product in product_dict:
                    selected.append(product_dict[product])
            selected = sorted(selected, key=lambda(x): float(x[1].split()[0][1:]))
            if context.portal_type == 'JazShopSelectStringField' and context.fgDefault:
                selected.insert(0, ('{}|0'.format(context.fgDefault), context.fgDefault))
            return selected
        """


# Action factory used by the UI for adding a new easyform action
JazShopCheckoutAction = ActionFactory(
    JazShopCheckout,
    _(u"label_jazshopcheckout_action", default=u"Checkout with jazkarta.shop"),
    "jazkarta.easyformplugin.jazshop.AddJazShopCheckoutActions",
)


# Supermodel handler for serializing the action configuration to an XML model
JazShopCheckoutHandler = BaseHandler(JazShopCheckout)




# XXX TODO REGISTER THESE EVENTS
'''
def add_checkout_redirect_after_creation(adapter, event):
    redirect_to = 'redirect_to:string:${portal_url}/checkout'
    success_override = adapter.aq_parent.getThanksPageOverride()
    if success_override:
        message = """By default, this adapter redirects the user to
            the Jazkarta Shop checkout after a successful submission.
            However, this form already has an active override. The
            checkout override was not added. Please see the documentation
            for information on how to set it manually."""
        messages = IStatusMessage(event.object.REQUEST)
        messages.add(message)
    else:
        adapter.aq_parent.setThanksPageOverride(redirect_to)
'''

"""
def handle_item_removed(event):
    cart = event.object
    # bail out if no pfg_forms involved
    if not 'pfg_forms' in cart.data:
        return
    order_details = ''
    cart_products = [i.uid for i in cart.items]
    for form_uid in cart.data['pfg_forms'].keys():
        form_products = cart.data['pfg_products'][form_uid]
        in_cart = True
        for p in form_products:
            if p not in cart_products:
                in_cart = False
        if in_cart:
            order_details += cart.data['pfg_details'][form_uid]
    cart.data['order_details'] = order_details
    cart.save()
"""
