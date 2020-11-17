import logging
from stock import Stock
from stock_statistics import StockStatistics
from csv_processor import CsvProcessor
from portfolio_search import PortfolioSearch

# Print utility
tabs = "\t\t\t"
tab = "\t"

# Set default logging level
logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

# Initialize components
stockStatistics = StockStatistics(years=0)
processor = CsvProcessor(stockStatistics=stockStatistics)
stocks = processor.load()
portfolio = PortfolioSearch()

# Display stock statistics
for stock in stocks:
  logger.debug(
      f'{stock.name} {tabs if len(stock.name) < 15 else tab} E[r] = {stock.expectedReturn} \t Std[r] = {stock.standardDeviation}')

# Run the search
portfolio, expReturn, std = portfolio.search(stocks, [], 0.01, 2.1)
logger.info(
    f"The following portfolio will give you E[r] = {expReturn} with Std[r] = {std}")

# Display the resulting portfolio
for asset in portfolio:
  logger.info(f"{asset[0] * 100}% {tab} {asset[1].name}")
