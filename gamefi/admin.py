# -*- coding: utf-8 -*-


from django.contrib import admin

# Register your models here.

from django.conf.urls import url
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.helpers import ActionForm
from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms
from django.db.models import Max
from collections import OrderedDict
import subprocess
import logging,traceback,json
logger = logging.getLogger(__name__)

from .models import Game, Account, GameSettlement, GameAccount

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'chain', 'token', 'url', 'account_cnt', 'input', 'output_game_token', 'last_game_token_balance', 'chain_balance', 'game_balance', 'token_price', 'game_balance_usd', 'game_balance_chain', 'ratio')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'game', 'address', 'chain_token_balance', 'game_token_balance', 'game_token_balance_not_claimed')
    list_filter = ('game',)

class GameAccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'game', 'address', 'game_token_balance', 'game_token_balance_not_claimed')
    list_filter = ('game',)

class GameSettlementAdmin(admin.ModelAdmin):
    list_display = ('game', 'last_game_token_balance', 'game_token_income', 'game_token_payout', 'game_token_balance', 'settle_time')
    list_filter = ('game',)


admin.site.register(Game, GameAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(GameSettlement, GameSettlementAdmin)
admin.site.register(GameAccount, GameAccountAdmin)


