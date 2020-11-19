import numpy as np

#INF = 2147483647
INF = 1000000


def logGeoMean(data):
  # Using log version of geometric mean to avoid overflow
  a = np.log(data)
  return np.exp(a.sum()/len(a))


def getCorrelation(key1, key2, correlations):
  keyFormat1 = f"{key1}-{key2}"
  if keyFormat1 in correlations.keys():
    return correlations[keyFormat1]
  else:
    return correlations[f"{key2}-{key1}"]
