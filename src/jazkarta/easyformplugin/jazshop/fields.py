from . import _
from zope.interface import implementer
from zope.schema import TextLine
from zope.schema import Field
from plone.schemaeditor.fields import FieldFactory
from plone.supermodel.exportimport import BaseHandler

from .interfaces import ILikert

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
