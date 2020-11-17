

class PortfolioSearch:
  """ Searches best combination of stocks given investor's:
    - criteria 
    - expected return
    - risk aversion
  """

  def __init__(self):
    self.maxExpReturn = 0.0
    self.maxStd = 0.0
    self.maxPortfolio = []
    self.portfolio = []

  def search(self, stocks, criteria, expReturn, risk):
    """ Search method to find best combination of stocks using
    iterative deepening depth first branch and bound algorithm.
    :param stocks: List of stocks statistics
    :param criteria: List of investor's criteria
    :param expReturn: Investor's expected return
    :param risk: Investor's risk aversion
    """

    for depth in range(len(stocks)):
      self.dfbnb(0, depth, 0)

    self.maxPortfolio.append((1, stocks[0]))
    return self.maxPortfolio, self.maxExpReturn, self.maxStd

  def dfbnb(self, depth, maxDepth, cost):
    pass
