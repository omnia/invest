import portfolio_statistics as stats
import math
import utils


class PortfolioSearch:
  """ Searches the best stock allocation for given capital
  and optionally specific investor's constraints.
  """

  def __init__(self, args):
    self.sharesIncrement = args["shares"]
    self.capital = args["capital"]
    self.riskAversion = args["risk"]
    self.diversify = args["diversify"]
    self.bestExpectedReturn = 0.0
    self.bestStandardDeviation = 0.0
    self.bestPerformance = utils.INF
    self.optimalPortfolio = {}
    self.portfolio = {}

  def search(self, stocks, correlations):
    """ Search method to find best combination of stocks using
    iterative deepening depth first branch and bound algorithm.
    :param stocks: Dictionary of stocks statistics
    :param criteria: List of investor's criteria
    :param expReturn: Investor's expected return
    :param risk: Investor's risk aversion"""

    def costLimitedSearch(depth):
      nonlocal stocksArr

      # Find out what is the maximum number of share we can buy
      maxShares = math.floor(
          (self.capital - sum(self.portfolio.values())) / stocksArr[depth].price)

      # Check for leaf node
      if depth == (len(stocksArr) - 1):
        # Leaf because no more stocks to look at
        self.portfolio[stocksArr[depth].symbol] = maxShares * \
            stocksArr[depth].price

        # Check portfolio performance score
        performance = stats.performance(self.portfolio, stocks,
                                        correlations, self.riskAversion,
                                        self.diversify)

        if performance < self.bestPerformance:
          self.bestPerformance = performance
          self.optimalPortfolio = self.portfolio.copy()

        self.portfolio[stocksArr[depth].symbol] = 0

        return

      if maxShares <= 0:
        # Leaf because we don't have more capital to allocate
         # Check portfolio performance score
        performance = stats.performance(self.portfolio, stocks,
                                        correlations, self.riskAversion,
                                        self.diversify)

        if performance < self.bestPerformance:
          self.bestPerformance = performance
          self.optimalPortfolio = self.portfolio.copy()

        return

      # Find increment steps
      increment = math.floor(maxShares * self.sharesIncrement)
      if increment <= 0:
        increment = maxShares

      # Loop over different amount of shares to buy and check the
      # portfolio performance. Start with 0 to allow for skipping of share.
      for shares in range(0, maxShares+1, increment):
        # Buy stocks
        sharesPrice = shares * stocksArr[depth].price
        self.portfolio[stocksArr[depth].symbol] = sharesPrice

        # Check portfolio performance score
        performance = stats.performance(self.portfolio, stocks,
                                        correlations, self.riskAversion,
                                        self.diversify)

        # If the current portfolio configuration performance
        # is lower than our previous best performance continue.
        if performance < self.bestPerformance or performance == utils.INF:
          costLimitedSearch(depth+1)

        self.portfolio[stocksArr[depth].symbol] = 0.0

      return

    stocksArr = list(stocks.values())

    # for depth in range(len(stocks)):
    #   self.depthLimitedSearch(0, depth, 0)

    costLimitedSearch(0)

    return self.optimalPortfolio, self.bestPerformance
