# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

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
