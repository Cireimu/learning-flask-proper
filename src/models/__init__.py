# -*- coding: utf-8 -*-

try:
    from .models import User, Restaurant, Menu_Item, Review, Restaurant_Item, Restaurant_Review
except ImportError:
    from .models import User, Restaurant, Menu_Item, Review, Restaurant_Item, Restaurant_Review