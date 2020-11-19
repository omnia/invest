import logging
import argparse
import numpy as np
from stock import Stock
from stock_statistics import StockStatistics
from csv_processor import CsvProcessor
from portfolio_search import PortfolioSearch
import portfolio_statistics as portfolioStats

# The main program.
# Set up and parse command-line arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--capital",  default=100000,
                help="Capital to invest.", type=int)
ap.add_argument("-s", "--shares", default=0.1,
                help="Percentage to increment shares to control the search tree breadth size", type=float)
ap.add_argument("-y", "--years", default=0,
                help="Historical years to use", type=int)
ap.add_argument("-d", "--diversify", default=3,
                help="Minimum number of assets to be allocated to.", type=int)
# ap.add_argument("-c", "--criteria", default="",
#                 help="Investors criteria", type=str)
ap.add_argument("-r", "--risk", default=1,
                help="""Risk aversion a float value.
                        Risk lover < 0. 
                        Risk neutral = 0. 
                        Risk averse > 0.""",
                type=float)
ap.add_argument("-v", "--verbose",
                help="Increase output verbosity.", action="store_true")
args = vars(ap.parse_args())
print(args)

# Set default logging level
logging.basicConfig(level="DEBUG" if args['verbose'] else "INFO")
logger = logging.getLogger(__name__)

# Initialize components
stockStatistics = StockStatistics(years=args["years"])
processor = CsvProcessor(stockStatistics=stockStatistics)
stocks, correlations = processor.load()
portfolio = PortfolioSearch(args)

# Display stock statistics
for i, (key, stock) in enumerate(stocks.items()):
  logger.info(
      f"{' ' if i < 10 else ''}{i} {stock.name.ljust(21, ' ')} \t Price = {stock.price}   \t E[r] = {stock.expectedReturn} \t Std[r] = {stock.standardDeviation}")

# Run the search
portfolio, performance = portfolio.search(stocks, correlations)
logger.debug(f"Performance {performance} \n{portfolio}")

weights, assetsCount = portfolioStats.getWeights(portfolio)

if assetsCount <= 0:
  logger.error(f"No valid solution given the investor's criteria")
  exit(1)

expectedReturn = portfolioStats.getExpectedReturn(portfolio, weights, stocks)
standardDeviation = portfolioStats.getStandardDeviation(
    portfolio, weights, stocks, correlations)
# Display the resulting portfolio
logger.info(
    f"The following portfolio will give you E[r] = {expectedReturn} with Std[r] = {standardDeviation}")


invested = sum(portfolio.values())
for key, value in portfolio.items():
  logger.info(
      f"{stocks[key].name.ljust(21, ' ')} \t {str(round(value / invested * 100, 4)).ljust(7, ' ')} % \t {portfolio[key]} kr.")
logger.info(
    f"{'Total'.rjust(21, ' ')} \t {round(sum(weights.values()) * 100,2)} % \t {round(invested,2)} kr.")
