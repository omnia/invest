import numpy as np
import math
import utils


def performance(portfolio, stocks, correlations, riskAversion, diversify):
  """ Calculates portfolio performance using a modified utility formula:
  Score = -1 * (E[r] - 1/2 * A * σ^2 * D)
  """
  weights, assetsCount = getWeights(portfolio)

  if assetsCount < diversify:
    return utils.INF

  expectedReturn = getExpectedReturn(portfolio, weights, stocks)
  standardDeviation = getStandardDeviation(
      portfolio, weights, stocks, correlations)
  diversifyFactor = 1 / math.log2(assetsCount)

  return -1 * (expectedReturn - (1/2 * riskAversion *
                                 (standardDeviation ** 2) * diversifyFactor))


def getWeights(portfolio):
  """ Given a portfolio of investments calculates it's weights."""
  capital = sum(portfolio.values())
  weights = {}

  for key, value in portfolio.items():
    weights[key] = value/capital if value > 0 else 0

  assetsCount = sum(1 if w > 0.0 else 0 for w in list(weights.values()))

  return weights, assetsCount


def getExpectedReturn(portfolio, weights, stocks):
  """ Given a portfolio, it's weights and stock information
  this function calculates the expected return.
  """
  portfolioReturn = 0.0

  for key in portfolio.keys():
    portfolioReturn += weights[key] * stocks[key].expectedReturn

  return portfolioReturn


def getStandardDeviation(portfolio, weights, stocks, correlations):
  sigma = np.array(getSigma(portfolio, stocks, correlations))
  weights = np.array(list(weights.values()))
  portfolioVar = np.matmul(np.transpose(weights),
                           np.matmul(sigma, weights))

  return math.sqrt(portfolioVar)


def getSigma(portfolio, stocks, correlations):
  sigma = [[0 for a in portfolio] for a in portfolio]

  for i, key in enumerate(portfolio.keys()):
    for j, otherKey in enumerate(portfolio.keys()):

      if (key == otherKey):
        sigma[i][j] = stocks[key].standardDeviation ** 2
      else:
        sigma[i][j] = stocks[key].standardDeviation * \
            stocks[otherKey].standardDeviation * \
            utils.getCorrelation(key, otherKey, correlations)

  return sigma
