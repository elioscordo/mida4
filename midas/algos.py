
from midas.models import Scanner, ScannerRun, Indicator


def run_algo(scanner):
    Algo = ALGOS[scanner.algo]
    algo = Algo()
    algo.run(scanner)


class Panda:
    def run(self, scanner, now=None):
        algo = 'panda'
        symbols = scanner.get_all_symbols()
        rsi = Indicator.get_or_load("RSI")
        for symbol in symbols:
            symbol_data = symbol.fetch_data(now)
            rsi.process(symbol_data)
        run = ScannerRun.objects.create(
            log=str(locals())
        )
        scanner.runs.add(run)


ALGOS = {
    Scanner.ALGO_PANDA: Panda
}
