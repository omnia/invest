import logging
from stock import Stock
from stock_statistics import StockStatistics
from csv_processor import CsvProcessor

# Set default logging level
logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

stockStatistics = StockStatistics(years=0)
processor = CsvProcessor(stockStatistics=stockStatistics)
stocks = processor.load()

tabs = "\t\t\t"
tab = "\t"

for stock in stocks:
  logger.debug(
      f'{stock.name} {tabs if len(stock.name) < 15 else tab} E[r] = {stock.expectedReturn} \t Std[r] = {stock.standardDeviation}')
