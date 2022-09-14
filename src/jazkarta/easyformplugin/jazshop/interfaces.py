# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.easyform.interfaces.actions import IAction
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from . import _

class IJazkartaEasyformpluginJazShopLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IJazShopCheckout(IAction):
    """Easyform action which places data in the jazkarta.shop cart"""
