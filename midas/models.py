
from django.db import models
from django.utils.translation import gettext_lazy as _
from talib import abstract
from midas.talib.proxy import get_indicators
from midas.alpaca.proxy import fetch_alpaca_data

TIMEFRAME_HOUR = "Hour"
TIMEFRAME_DAY = "Day"
TIMEFRAME_MINUTE = "Minute"


TIMEFRAME_CHOICES = (
    (TIMEFRAME_HOUR, "Hour"),
    (TIMEFRAME_DAY, "Day"),
    (TIMEFRAME_MINUTE, "Minute"),
)

TIMEFRAME_CHOICES = (
    (TIMEFRAME_HOUR, "Hour"),
    (TIMEFRAME_DAY, "Day"),
    (TIMEFRAME_MINUTE, "Minute"),
)

BROKER_ALPACA = "alpaca"

BROKERS = [
    (BROKER_ALPACA, "Alpaca")
]


class Symbol(models.Model):
    code = models.CharField(_("Code"), max_length=1023)
    name = models.CharField(_("Name"), max_length=1023, null=True)
    broker = models.CharField(choices=BROKERS, default=BROKER_ALPACA)
    exchange = models.CharField("Exchange", null=True, blank=True)
    json = models.JSONField(_("Json"), max_length=1023, null=True, blank=True)
    indexes = models.ManyToManyField("midas.Index", verbose_name=_("indexes"),
                                     related_name="symbol_index", blank=True)
    industries = models.ManyToManyField("midas.Industry", verbose_name=_("industries"),
                                        related_name="industry_index", blank=True)

    def __str__(self):
        return f"{self.code},{self.name}, {self.exchange}"

    def get_data(self, *args, **kwargs):
        return fetch_alpaca_data(self.code, *args, **kwargs)


class Scanner(models.Model):
    ALGO_PANDA = "algos.Panda"
    ALGO_CAT = "Cat"
    ALGO_COYOTE = "Coyote"

    ALGO_CHOICES = (
        (ALGO_PANDA, "Momentum Panda"),
        (ALGO_CAT, "Deep Cat"),
        (ALGO_COYOTE, "Coyote"),
    )
    STATUS_CHOICES = (
        ("on", "on"),
        ("off", "Off"),
    )

    name = models.CharField(_("Name"), max_length=1023)
    index = models.ForeignKey(
        "midas.Index", blank=True, null=True, on_delete=models.SET_NULL
    )
    time_frame = models.CharField(choices=TIMEFRAME_CHOICES,
                                  default=TIMEFRAME_HOUR)
    status = models.CharField(choices=STATUS_CHOICES, default="off")
    algo = models.CharField(
        choices=ALGO_CHOICES, blank=True, null=True
    )

    leads = models.ManyToManyField(
        "midas.Symbol",
        related_name="scanner_leads",
        blank=True
    )
    symbols = models.ManyToManyField(
        "midas.Symbol", verbose_name=_("Watchlist"),
        related_name="scanner_symbols",
        blank=True
    )
    runs = models.ManyToManyField(
        "midas.ScannerRun", verbose_name=_("ScannerRun"),
        related_name="scanner_runs",
        blank=True
    )
    indicator_conditions = models.ManyToManyField(
        "midas.IndicatorCondition",
        blank=True
    )
    indicator_instances = models.ManyToManyField(
        "midas.IndicatorInstance",
        blank=True
    )

    def run(self):
        from midas.algos import run_algo
        run_algo(self)

    def indicator_instances_str(self):
        return ','.join([i.name for i in self.indicator_instances.all()])

    def get_all_symbols(self):
        if self.symbols:
            return self.symbols

    def __str__(self):
        return self.name


class ScannerRun(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    log = models.JSONField(_("Log"))


class IndicatorCondition(models.Model):
    name = models.CharField(_("Name"), max_length=1023, blank=True)
    condition = models.JSONField(_("Preset"))
    code = models.CharField(_("Code"), max_length=1023, blank=True)
    indicator_instances = models.ManyToManyField(
        "midas.IndicatorInstance",
        blank=True
    )

    def __str__(self):
        return self.code


class IndicatorInstance(models.Model):
    name = models.SlugField(_("Name"), unique=True, max_length=1023)
    setup = models.JSONField(_("Setup"), blank=True, null=True)
    indicator = models.ForeignKey("midas.Indicator",
                                  blank=True, null=True,
                                  on_delete=models.CASCADE)
    code = models.TextField(_("Code"), blank=True, null=True)
    options = models.TextField(_("Options"), blank=True, null=True)

    def __str__(self):
        return self.name

    def process(self, df):
        if self.indicator.lib == self.indicator.LIB_TALIB:
            indicator = abstract.Function(self.indicator.code)
            if not self.setup:
                data = indicator(df)
            else:
                data = indicator(df, **self.setup)
            return data
        return []


class Indicator(models.Model):
    LIB_TALIB = "talib"

    code = models.CharField(
        _("Code"), max_length=1023, blank=True, null=True
    )
    group = models.CharField(
        _("Group"), max_length=1023, blank=True, null=True
    )
    lib = models.CharField(
        _("Library"), max_length=1023, blank=True, null=True
    )

    @classmethod
    def get_or_load(cls, code):
        indicators = cls.objects.filter(code=code)
        if indicators.exists():
            return indicators.first()
        return cls.load(code)
        # attempt to load

    @classmethod
    def load(cls, code):
        if code in get_indicators():
            return cls.objects.create(
                        code=code,
                        group=None,
                        lib=cls.LIB_TALIB
                    )

    def __str__(self):
        return f"{self.code},{self.group},{self.lib}"


class Index(models.Model):
    ticker = models.CharField(
        _("Ticker"), max_length=1023, blank=True, null=True
    )
    name = models.CharField(
        _("Name"), max_length=1023, blank=True, null=True
    )
    log = models.TextField(
        _("Log"), null=True, blank=True
    )

    def __str__(self):
        return f"{self.ticker}"


class Industry(models.Model):
    name = models.CharField(
        _("Name"), max_length=1023, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}"
