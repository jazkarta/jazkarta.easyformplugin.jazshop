from . import _
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ITerms
from z3c.form.interfaces import IWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.select import SelectFieldWidget
from zope.component import adapter
from zope.component import queryUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import TextLine
from zope.schema import Field
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone.schemaeditor.fields import FieldFactory
from plone.supermodel.exportimport import BaseHandler

from .interfaces import IJazShopProductSelect
from .interfaces import ILikert


@implementer(IJazShopProductSelect)
class JazShopProductSelect(TextLine):
    """A Product Selection Field"""
    use_radio = False
    available_products = ()
    vocabularyName = None

    def __init__(self, **kwargs):
        self.use_radio = kwargs.pop('use_radio', False)
        self.available_products = kwargs.pop('available_products', ())
        Field.__init__(self, **kwargs)


@implementer(ITerms)
@adapter(Interface, IFormLayer, Interface, IJazShopProductSelect, IWidget)
def JazShopProductSelectTerms(context, request, form, field, widget):
    vocab_factory = queryUtility(
        IVocabularyFactory,
        name=u'jazkarta.easyformplugin.jazshop.vocabs.available_products'
    )
    if vocab_factory is not None:
        vocab = vocab_factory(context)
        return SimpleVocabulary([
            vocab.getTerm(v) for v in field.available_products
        ])
    return SimpleVocabulary([])


JazShopProductSelectFactory = FieldFactory(
    JazShopProductSelect, _(u"Product Selection")
)
JazShopProductSelectHandler = BaseHandler(JazShopProductSelect)


@adapter(IJazShopProductSelect, IFormLayer)
@implementer(IFieldWidget)
def JazShopProductSelectFieldWidget(field, request):
    if field.use_radio:
        return RadioFieldWidget(field, request)
    return SelectFieldWidget(field, request)


@implementer(ILikert)
class Likert(TextLine):
    """A Likert field"""

    def __init__(self, **kwargs):
        self.answers = kwargs.get('answers', None)
        if 'answers' in kwargs:
            del kwargs['answers']
        self.questions = kwargs.get('questions', None)
        if 'questions' in kwargs:
            del kwargs['questions']
        Field.__init__(self, **kwargs)

    def _validate(self, value):
        super(Likert, self)._validate(value)
        self.parse(value)

    def parse(self, value):
        result = dict()
        lines = value.split(',')
        for line in lines:
            if not line:
                continue
            id, answer = line.split(':')
            answer = answer.strip()
            if answer not in self.answers:
                raise ValueError('Invalid answer value.')
            index = int(id)
            if index < 1 or index > len(self.questions):
                raise ValueError('Invalid question index.')
            result[index] = answer
        return result


LikertFactory = FieldFactory(
    Likert, _(u"label_likert_field", default=u"Likert")
)
LikertHandler = BaseHandler(Likert)
