import z3c.form
from collective.easyform.interfaces.actions import IAction
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.schemaeditor.schema import ITextLinesField
from zope.schema.interfaces import IField
from zope import schema, interface

from . import _


class IJazkartaEasyformpluginJazShopLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IJazShopCheckout(IAction):
    """Easyform action which places data in the jazkarta.shop cart"""
    formIdExpression = schema.TextLine(
        title=_(u'Form id expression'),
        description=_(u'An expression used to mark products in the cart. You can include field contents with {field_name}'),
        required=False,
    )


class IJazShopProductSelect(IField):

    available_products = schema.Tuple(
        title=_(u'Available Products'),
        value_type=schema.Choice(
            vocabulary=u'jazkarta.easyformplugin.jazshop.vocabs.available_products',
        ),
        required=False,
        default=(),
    )

    use_radio = schema.Bool(
        title=_(u'Use radio buttons?'),
        description=_(u'Use a radio widget instead of a select dropdown, '
                      u'best for lists of 5 or fewer prodcuts.'),
        required=False,
        default=False,
    )


product_select_field = z3c.form.util.getSpecification(
    IJazShopProductSelect['available_products']
)


class IJazShopProductMultiSelect(IJazShopProductSelect):

    use_radio = schema.Bool(
        title=_(u'Use checkbox selection?'),
        description=_(u'Use a checkbox widget instead of a multi-select dropdown, '
                      u'best for lists of 5 or fewer prodcuts.'),
        required=False,
        default=False,
    )


class ILikert(IField):

    questions = schema.List(
        title=_(u'Possible questions'),
        description=_(u'Enter allowed choices one per line.'),
        required=schema.interfaces.IChoice['vocabulary'].required,
        default=schema.interfaces.IChoice['vocabulary'].default,
        value_type=schema.TextLine())
    interface.alsoProvides(questions, ITextLinesField)

    answers = schema.List(
        title=_(u'Possible answers'),
        description=_(u'Enter allowed choices one per line.'),
        required=schema.interfaces.IChoice['vocabulary'].required,
        default=schema.interfaces.IChoice['vocabulary'].default,
        value_type=schema.TextLine())
    interface.alsoProvides(answers, ITextLinesField)


class ILikertWidget(z3c.form.interfaces.IWidget):
    """Likert widget."""
