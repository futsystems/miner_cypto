# -*- coding: utf-8 -*-


from django.contrib import admin

import logging
logger = logging.getLogger(__name__)

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'price_source', 'price_symbol', 'current_price')


admin.site.register(Token, TokenAdmin)