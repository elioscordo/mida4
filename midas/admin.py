
from django.contrib import admin
from midas.models import Symbol, Indicator, Scanner, IndicatorCondition, \
    IndicatorInstance, Index, Industry
from unfold.admin import ModelAdmin
from midas.alpaca.proxy import get_all_assets, asset_to_dict
from midas.talib.proxy import get_grouped_indicators
from django.urls import path
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.utils.html import format_html

from pytickersymbols import PyTickerSymbols

@admin.register(Scanner)
class ScannerAdmin(ModelAdmin):
    autocomplete_fields = ['leads', 'symbols', 'indicator_instances']
    list_display = ('name', 'dashboard_link')

    def dashboard_link(self, item):
        out = render_to_string(
            'midas/scanner/dashboard_link.html',
            {'item': item}
        )
        return format_html(
            out
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<path:object_id>/dashboard/",
                self.admin_site.admin_view(self.my_view),
                name="midas_scanner_dashboard"
                )
            ]
        return my_urls + urls

    def my_view(self, request, object_id):
        scanner = Scanner.objects.get(pk=object_id)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
        )
        context["item"] = scanner
        return TemplateResponse(
            request, "midas/scanner/dashboard.html", context
        )


@admin.register(IndicatorCondition)
class IndicatorConditionAdmin(ModelAdmin):
    pass


@admin.register(IndicatorInstance)
class IndicatorInstanceAdmin(ModelAdmin):
    autocomplete_fields = ['indicator',]
    search_fields = ['name',]

@admin.register(Indicator)
class IndicatorAdmin(ModelAdmin):
    search_fields = ['code',]
    actions = ['refresh_talib',]

    def refresh_talib(self, request, queryset):
        library = Indicator.LIB_TALIB
        for group, names in get_grouped_indicators():
            for name in names:
                if not Indicator.objects.filter(code=name, lib=library).exists():
                    Indicator.objects.create(
                        code=name,
                        group=group,
                        lib=library
                    )
    refresh_talib.short_description = "Load talib Indicators"


@admin.register(Symbol)
class SymbolAdmin(ModelAdmin):
    actions = ['refresh_alpaca',]
    list_filter = ['exchange']
    search_fields = ['code', 'name', 'exchange']
    list_display = ('code', 'name', 'exchange')
    autocomplete_fields = ['indexes', 'industries']

    def refresh_alpaca(self, request, queryset):
        for asset in get_all_assets():
            if not Symbol.objects.filter(code=asset.symbol).exists():
                Symbol.objects.create(
                    name=asset.name,
                    code=asset.symbol,
                    exchange=asset.exchange,
                    json=asset_to_dict(asset),
                    broker="alpaca"
                )
    refresh_alpaca.short_description = "Load Alpaca Symbols"



@admin.register(Index)
class IndexAdmin(ModelAdmin):
    actions = ['tag_symbols', 'reload_indexes']
    list_display = ('name', 'ticker', 'symbol_count')
    search_fields = ['name', 'ticker']

    def tag_symbols(self, request, queryset):
        stock_data = PyTickerSymbols()
        for item in queryset:
            index_symbols = list(stock_data.get_stocks_by_index(item.ticker))
            index_ticker_set = set([item["symbol"] for item in index_symbols])
            symbols = Symbol.objects.filter(code__in=index_ticker_set)
            found = []
            for symbol in symbols:
                symbol.indexes.add(item)
                found.append(symbol.code)
            not_found = index_ticker_set - set(found)
            item.log = f"{item.log}  \n  not found {not_found}"
            item.save()

    def reload_indexes(self, request, queryset):
        stock_data = PyTickerSymbols()
        items = stock_data.get_all_indices()
        for item in items:
            Index.objects.create(
                ticker=item,
                name=item
            )

    def symbol_count(self, item):
        return item.symbol_index.all().count()

    tag_symbols.short_description = "Include symbols"
    reload_indexes.short_description = "Reload indexes with pyticker"


@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
