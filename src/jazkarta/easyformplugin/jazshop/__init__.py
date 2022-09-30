# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("jazkarta.easyformplugin.jazshop")


from .interfaces import ILikert  # noqa
from .interfaces import ILikertWidget  # noqa

from .monkeypatch import patch_easyform


patch_easyform()
