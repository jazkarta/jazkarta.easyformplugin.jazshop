from . import _
from decimal import Decimal
from decimal import InvalidOperation
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ITerms
from z3c.form.interfaces import IWidget
from z3c.form.term import Terms
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.select import SelectFieldWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget as PloneSelectFieldWidget
from zope.component import adapter
from zope.component import queryUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema import Field
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone.schemaeditor.fields import FieldFactory
from plone.supermodel.exportimport import BaseHandler

from .interfaces import IJazShopProductSelect
from .interfaces import IJazShopProductMultiSelect
from .interfaces import IJazShopArbitraryPriceStringField

from six import PY3

@implementer(IJazShopProductSelect)
class JazShopProductSelect(TextLine):
    """A Product Selection Field"""
    use_radio = False
    available_products = ()

    def __init__(self, **kwargs):
        self.use_radio = kwargs.pop('use_radio', False)
        self.available_products = kwargs.pop('available_products', ())
        Field.__init__(self, **kwargs)


@implementer(ITerms)
@adapter(Interface, IFormLayer, Interface, IJazShopProductSelect, IWidget)
def JazShopProductSelectTerms(context, request, form, field, widget):
    terms = Terms()
    vocab_factory = queryUtility(
        IVocabularyFactory,
        name=u'jazkarta.easyformplugin.jazshop.vocabs.available_products'
    )
    # FIXME This approach is quite inefficient: to build the vocabulary
    # of the products available on this form (the ones the user selected)
    # we're currently starting from a vocabulary that includes all products on the site,
    # that needs to query the catalog to get info about all.
    # It would make sense to only query the products we care about
    # (the ones in `field.available_products`).
    if vocab_factory is not None:
        vocab = vocab_factory(context)
        new_items = []
        for vocab_item in field.available_products:
            try:
                new_items.append(vocab.getTerm(vocab_item))
            except LookupError:
                pass
        terms.terms = SimpleVocabulary(new_items)
    else:
        terms.terms = SimpleVocabulary([])
    return terms


@adapter(IJazShopProductSelect, IFormLayer)
@implementer(IFieldWidget)
def JazShopProductSelectFieldWidget(field, request):
    if field.use_radio:
        return RadioFieldWidget(field, request)
    return SelectFieldWidget(field, request)


JazShopProductSelectFactory = FieldFactory(
    JazShopProductSelect, _(u"Product Selection")
)
JazShopProductSelectHandler = BaseHandler(JazShopProductSelect)


@implementer(IJazShopProductMultiSelect)
class JazShopProductMultiSelect(Tuple):
    """A Product Multi-selection Field"""

    __init__ = JazShopProductSelect.__dict__['__init__'] if PY3 else JazShopProductSelect.__init__.im_func


@adapter(IJazShopProductMultiSelect, IFormLayer)
@implementer(IFieldWidget)
def JazShopProductMultiSelectFieldWidget(field, request):
    if field.use_radio:
        return CheckBoxFieldWidget(field, request)
    return PloneSelectFieldWidget(field, request)


JazShopProductMultiSelectFactory = FieldFactory(
    JazShopProductMultiSelect, _(u"Multiple Product Selection")
)
JazShopProductMultiSelectHandler = BaseHandler(JazShopProductMultiSelect)


@implementer(IJazShopArbitraryPriceStringField)
class JazShopArbitraryPriceStringField(TextLine):
    """Arbitrary price field (suitable for donations)"""

    available_products = ()

    def _validate(self, value):
        super(JazShopArbitraryPriceStringField, self)._validate(value)
        try:
            Decimal(value.replace("$", ""))
        except InvalidOperation:
            raise Invalid(_("invalid_price", "Please insert a number"))

    def __init__(self, **kwargs):
        self.available_products = kwargs.pop('available_products', ())
        TextLine.__init__(self, **kwargs)


JazShopArbitraryPriceStringFieldFactory = FieldFactory(
    JazShopArbitraryPriceStringField, _(u"label_arbitraty_price_field", default=u"Arbitrary price")
)
JazShopArbitraryPriceStringFieldHandler = BaseHandler(JazShopArbitraryPriceStringField)
