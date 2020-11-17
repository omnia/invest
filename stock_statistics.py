from datetime import datetime
import statistics as stats
from stock import Stock
import numpy as np
import math


class StockStatistics:

  def __init__(self, years=0):
    """ Constructor
    years: Uses historical value from 'today' to 'today - years'.
           Default value is 0, meaning it uses all available data.
    """
    self.years = years

  def calculate(self, stockData, stock):
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
    stock.setStatistics(logGeoMean(
        grossReturns) ** 365 - 1, stats.pstdev(returns) * math.sqrt(250))


def logGeoMean(data):
  # Using log version of geometric mean to avoid overflow
  a = np.log(data)
  return np.exp(a.sum()/len(a))
