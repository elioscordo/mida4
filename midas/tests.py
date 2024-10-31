from django.test import TestCase
from midas.models import Scanner, Symbol


class PandaScannerCase(TestCase):

    def setUp(self):
        tesla = Symbol.objects.create(code="TSL")
        marathon = Symbol.objects.create(code="MARA")
        self.symbols = [tesla, marathon]
        self.scanner = Scanner.objects.create(
            algo=Scanner.ALGO_PANDA
        )
        self.scanner.symbols.set(self.symbols)

    def test_run(self):
        self.scanner.run()
