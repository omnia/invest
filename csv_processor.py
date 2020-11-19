import pathlib
import logging
import pandas as pd
import numpy as np
from stock import Stock
from stock_statistics import StockStatistics
from datetime import datetime


class CsvProcessor:
  def __init__(self, stockStatistics=StockStatistics(), path="data/*.csv"):
    self.logger = logging.getLogger(__name__)
    self.path = path
    self.separator = ";"
    self.stockStatistics = stockStatistics

    self.logger.debug(
        f"CSV processor setup to use data from '{self.path}' using separator '{self.separator}'")

  def load(self):
    self.logger.debug(f"Start data processing from {self.path} data files")

    dataFiles = list(pathlib.Path().glob(self.path))

    stocks = {}
    stocksData = {}
    for filePath in dataFiles:
      self.logger.debug(f"Reading data from {filePath}")
      stock = self.initStockMetadata(filePath)
      stockData = pd.read_csv(filePath, sep=';', skiprows=1, usecols=[
          'Date', 'Closing price'], parse_dates=['Date'],
          dtype={'Closing price': np.float64}, decimal=',')
      stockData = self.stockStatistics.getStockBasicStats(
          stockData.to_numpy(), stock)
      stocks[stock.symbol] = stock
      stocksData[stock.symbol] = stockData

    correlation = self.stockStatistics.correlation(stocksData)

    self.logger.info(f"Processed {len(dataFiles)} data files")

    return stocks, correlation

  def initStockMetadata(self, filePath):
    stock = None
    # Read metadata
    with open(filePath) as file:
      # First line contains metadata for the corresponding stock
      metadataLine = file.readline()
      metadata = metadataLine.split(self.separator)
      stock = Stock(metadata[0], metadata[1], metadata[2])

    return stock
