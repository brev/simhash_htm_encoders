import numpy as np

### https://github.com/vsraptor/bbhtm/blob/master/lib/stats.py
### https://stackoverflow.com/questions/47648133/mape-calculation-in-python


# Mean absolute error : mae(ys, yhat)
def mae(ys, yhat): 
  ys = np.array(ys) 
  yhat = np.array(yhat)
  return np.mean(np.abs(ys - yhat))

# Mean absolute percentage error : mape(ys, yhat)
def mape(ys, yhat): 
  ys = np.array(ys) 
  yhat = np.array(yhat)
  return np.mean(np.abs((ys - yhat) / ys))

# Negative Log Likelihood : nll(ys, yhat, bins)
def nll(ys, yhat, bins=1000):
  ys = np.array(ys) 
  yhat = np.array(yhat)
  assert ys.size == yhat.size

  counts, ranges = np.histogram(yhat, bins=bins)
  total =  ys.size
  probs = np.zeros(yhat.size)

  for (i, n) in enumerate(ys) :
    in_bins = np.argwhere(n < ranges)

    #which bin to use to calculate probabilities
    if len(in_bins) == 0 : in_bin = counts.size - 1 #above range
    else : in_bin = in_bins[0][0] - 1 #-1 because ranges.size == bins.size + 1

    if counts[in_bin] == 0 : probs[i] = 1.0 #log(1) = 0
    else : probs[i] = counts[in_bin]  / float(total)

  return - np.average(np.log(probs))

# Root mean square error : rmse(ys, yhat)
def rmse(ys, yhat): 
  ys = np.array(ys) 
  yhat = np.array(yhat)
  return np.sqrt(np.mean(np.power((ys - yhat), 2)))

