# -*- coding: utf-8 -*-

try:
    from .auth import *
    from .restaurants import *
    from .reviews import *
except ImportError:
    from .auth import *
    from .restaurants import *
    from .reviews import *