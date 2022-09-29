import logging
from collective.easyform.actions import Action, ActionFactory
from collective.easyform.api import get_context, get_schema
from plone.app.uuid.utils import uuidToObject
from plone.schemaeditor.utils import FieldAddedEvent, FieldRemovedEvent
from plone.supermodel.exportimport import BaseHandler
from zope.globalrequest import getRequest
from zope.interface import implementer
from jazkarta.shop.cart import Cart
from Products.statusmessages.interfaces import IStatusMessage

from . import _
from .interfaces import IJazShopCheckout
from .interfaces import IJazShopProductSelect
from .interfaces import IJazShopProductMultiSelect

logger = logging.getLogger(__name__)


@implementer(IJazShopCheckout)
class JazShopCheckout(Action):
    """easyform action that will add elements from the form to the jazkarta.shop cart.
    """

    def __init__(self, **kw):
        for name, field in IJazShopCheckout.namesAndDescriptions():
            setattr(self, name, kw.pop(name, field.default))
        super(JazShopCheckout, self).__init__(**kw)

    def get_form(self):
        return get_context(self)

    def _get_item_details(self, fields, request):
        form = self.get_form()
        schema = get_schema(form)

        details = '<p></p><h2>{}</h2><dl>\n'.format(form.title)
        shop_fields = []
        for field in schema:
            if IJazShopProductMultiSelect.providedBy(schema[field]) or IJazShopProductSelect.providedBy(schema[field]):
                label = schema.get(field).title
                value = fields[field]
                shop_fields.append(field)
                details += '<dt>{}</dt><dd>{}</dd>\n'.format(label, uids_to_title(value))
        details += '</dl><p></p>\n'
        return shop_fields, details

    def get_cart(self, request=None):
        """Retrieve the cart object and make sure it's initialized for use with this action.
        """
        if request is None:
            request = getRequest()
        cart = Cart.from_request(request)
        if 'easyform_products' not in cart.data:
            cart.data['easyform_products'] = {}
        if 'easyform_details' not in cart.data:
            cart.data['easyform_details'] = {}
        if 'easyform_forms' not in cart.data:
            cart.data['easyform_forms'] = {}
        return cart

    def onSuccess(self, fields, request):
        """ TODO
        """
        form = self.get_form()
        cart = self.get_cart(request)
        schema = get_schema(form)

        item_prepend = None
        if self.formIdExpression:
            try:
                item_prepend = self.formIdExpression.format(**fields)
            except (KeyError, ValueError):
                pass
        products = get_products(schema, fields)
        easyform_products = []
        for uid in products:
            if uid != '0':
                cart.add_product(uid)
                easyform_products.append(uid)
        if item_prepend is not None:
            for item in cart._items.values():
                if (item['uid'] in products and
                        not item['name'].startswith(item_prepend)):
                    item['name'] = item_prepend + item['name']
        form_uid = form.UID()
        cart.data['easyform_products'][form_uid] = easyform_products
        cart_fields, details = self._get_item_details(fields, request)
        cart.data['easyform_forms'][form_uid] = cart_fields
        cart.data['easyform_details'][form_uid] = details
        update_cart_data(cart)  # Will also save the cart for us

        # XXX Test this, see whats required and what is not
        """
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


def uids_to_title(values):
    titles = []
    if not isinstance(values, tuple) and not isinstance(values, list):
        values = [values]
    for value in values:
        try:
            titles.append(uuidToObject(value).title)
        except AttributeError:
            logger.error("UID not found while compiling cart summary: %s" % value)
    return ", ".join(titles)


def get_products(schema, fields):
    """Given a schema and field values, look into fields that belong to this add-on,
    extract and return the products that are selected
    """
    products = []
    for field in fields:
        if field not in schema:
            continue  # Should never happen
        if IJazShopProductMultiSelect.providedBy(schema[field]):
            products.extend(fields[field])
        elif IJazShopProductSelect.providedBy(schema[field]):
            products.append(fields[field])
    return products


# Action factory used by the UI for adding a new easyform action
JazShopCheckoutAction = ActionFactory(
    JazShopCheckout,
    _(u"label_jazshopcheckout_action", default=u"Checkout with jazkarta.shop"),
    "jazkarta.easyformplugin.jazshop.AddJazShopCheckoutActions",
)


# Supermodel handler for serializing the action configuration to an XML model
JazShopCheckoutHandler = BaseHandler(JazShopCheckout)




def add_checkout_redirect_after_creation(adapter, event):
    if not hasattr(event, "field") or not isinstance(event.field, JazShopCheckout):
        return
    redirect_to = 'string:${portal_url}/checkout'
    form = event.object.aq_parent.aq_base

    if isinstance(event, FieldAddedEvent):
        form.thanksPageOverrideAction = u'redirect_to'
        if form.thanksPageOverride is not None:
            if form.thanksPageOverride != redirect_to:
                message = """By default, this adapter redirects the user to
                    the Jazkarta Shop checkout after a successful submission.
                    However, this form already has an active override.
                    The current value is %s. The checkout override was not added.
                    Please see the documentation for information on how
                    to set it manually.""" % form.thanksPageOverride
                messages = IStatusMessage(event.object.REQUEST)
                messages.add(message)
        else:
            form.thanksPageOverride = redirect_to
    if isinstance(event, FieldRemovedEvent):
        form.thanksPageOverride = None


def handle_item_removed(event):
    update_cart_data(event.object)


def update_cart_data(cart):
    # bail out if no easyform_forms involved
    if not 'easyform_forms' in cart.data:
        return
    order_details = ''
    cart_products = [i.uid for i in cart.items]
    for form_uid in cart.data['easyform_forms']:
        form_products = cart.data['easyform_products'][form_uid]
        in_cart = True
        for p in form_products:
            if p not in cart_products:
                in_cart = False
        if in_cart:
            order_details += cart.data['easyform_details'][form_uid]
    cart.data['order_details'] = order_details
    cart.save()
