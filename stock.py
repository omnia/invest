
class Stock:
  def __init__(self, symbol, name, category):
    self.symbol = symbol
    self.name = name
    self.category = category
    self.expectedReturn = 0.0
    self.standardDeviation = 0.0

  def setStatistics(self, exReturn, std):
    self.expectedReturn = exReturn
    self.standardDeviation = std
