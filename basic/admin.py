# -*- coding: utf-8 -*-


from django.contrib import admin

import logging
logger = logging.getLogger(__name__)

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'precision', 'chain_type', 'contract_address', 'price_source', 'price_symbol', 'current_price')


admin.site.register(Token, TokenAdmin)