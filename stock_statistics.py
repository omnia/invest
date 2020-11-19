import numpy as np
import math
from scipy.stats import pearsonr
from datetime import datetime
import statistics as stats

from stock import Stock
import utils


class StockStatistics:

  def __init__(self, years=0):
    """ Constructor
    years: Uses historical value from 'today' to 'today - years'.
           Default value is 0, meaning it uses all available data.
    """
    self.years = years

  def getStockBasicStats(self, stockData, stock):
    """ Calculates stock's expected return and standard deviation
    from stock's historical data, optionally filtered by self.years.
    """
    dateFilter = None
    if self.years > 0:
      today = datetime.today()
      dateFilter = datetime(today.year - self.years, today.month, 1)
    else:
      dateFilter = datetime(1970, 1, 1)

    targetData = stockData[stockData[:, 0] >= dateFilter]
    returns = [(targetData[i, 1]/targetData[i+1, 1]) -
               1 for i in range(0, len(targetData)-1)]
    ones = np.ones(len(returns))
    grossReturns = ones + returns

    # Annualized statistics
    stock.price = targetData[0, 1]
    stock.expectedReturn = utils.logGeoMean(grossReturns) ** 365 - 1
    stock.standardDeviation = stats.pstdev(returns) * math.sqrt(250)

    return targetData[:, 1]

  def correlation(self, stocksData):
    """ Returns correlation coefficient dictionary for any two stocks.
    :param: stocksData - Dictionary where the key is the stock symbol
            and value is array of stock return
    """
    correlations = {}
    for key in stocksData.keys():
      for otherKey in stocksData.keys():
        if key == otherKey:
          continue

        key1 = f"{key}-{otherKey}"
        key2 = f"{otherKey}-{key}"

        if key1 in correlations.keys() or key2 in correlations.keys():
          continue

        if len(stocksData[key]) > len(stocksData[otherKey]):
          stocksData[key] = stocksData[key][0:len(stocksData[otherKey])]
        elif len(stocksData[key]) < len(stocksData[otherKey]):
          stocksData[otherKey] = stocksData[otherKey][0:len(stocksData[key])]

        correlations[key1] = pearsonr(stocksData[key], stocksData[otherKey])[0]

    return correlations
