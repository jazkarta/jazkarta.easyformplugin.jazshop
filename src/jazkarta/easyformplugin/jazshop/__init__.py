# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("jazkarta.easyformplugin.jazshop")


try:
    # patch are only needed in migration PFG->easyform
    # in python3 this will cause import error (PFG missing)
    from .monkeypatch import patch_easyform
    patch_easyform()
except:
    pass
