import csv
import datetime
import json
import numpy

from nupic.algorithms.sdr_classifier_factory import SDRClassifierFactory
from nupic.algorithms.spatial_pooler import SpatialPooler
from nupic.algorithms.temporal_memory import TemporalMemory
from nupic.encoders.adaptive_scalar import AdaptiveScalarEncoder
from nupic.encoders.date import DateEncoder
from nupic.encoders.random_distributed_scalar \
     import RandomDistributedScalarEncoder
from nupic.encoders.scalar import ScalarEncoder
from simhash_distributed_scalar import SimHashDistributedScalarEncoder
from stats import mae, mape, nll, rmse


# setup

COL_WIDTH = 2048

timeOfDayEncoder = DateEncoder(timeOfDay=(21, 1))
weekendEncoder = DateEncoder(weekend=21)
#consumeEncoder = RandomDistributedScalarEncoder(
#  n=400,
#  w=21,
#  resolution=0.4)   # best, 0.88 original
#consumeEncoder = ScalarEncoder(
#  n=400,
#  w=21,
#  minval=0,
#  maxval=100)
#consumeEncoder = AdaptiveScalarEncoder(
#  n=400,
#  w=21)
consumeEncoder = SimHashDistributedScalarEncoder(
  n=400,
  w=21,
  resolution=0.25)
encodingWidth = (
  timeOfDayEncoder.getWidth() +
  weekendEncoder.getWidth() +
  consumeEncoder.getWidth())
classifier = SDRClassifierFactory.create()
sp = SpatialPooler(
  inputDimensions=(encodingWidth,),
  columnDimensions=(COL_WIDTH),
  potentialPct=0.85,
  potentialRadius=encodingWidth,
  globalInhibition=True,
  localAreaDensity=-1.0,
  numActiveColumnsPerInhArea=40,
  synPermInactiveDec=0.005,
  synPermActiveInc=0.04,
  synPermConnected=0.1,
  boostStrength=3.0,
  seed=1956,
  wrapAround=False)
tm = TemporalMemory(
  columnDimensions=(COL_WIDTH,),
  cellsPerColumn=32,
  activationThreshold=16,
  initialPermanence=0.21,
  connectedPermanence=0.5,
  minThreshold=12,
  maxNewSynapseCount=20,
  permanenceIncrement=0.1,
  permanenceDecrement=0.1,
  predictedSegmentDecrement=0.0,
  maxSegmentsPerCell=128,
  maxSynapsesPerSegment=32,
  seed=1960)


# MAIN

with open('rec-center-hourly.csv', 'r') as fin:
  consumptions = []
  predictions = []
  prediction = None
  REZ = []
  hamming = {}

  reader = csv.reader(fin)
  next(reader)
  next(reader)
  next(reader)

  for (count, record) in enumerate(reader):
    if count >= 3000: break

    dateString = datetime.datetime.strptime(record[0], "%m/%d/%y %H:%M")
    consumption = float(record[1])

    if (prediction is not None) and (1==1):
      #print("row: %s %s %s" % (count, consumption, prediction))
      predictions.append(prediction)
      consumptions.append(consumption)

    # new empty encodings
    timeOfDayBits = numpy.zeros(timeOfDayEncoder.getWidth(), numpy.uint8)
    weekendBits = numpy.zeros(weekendEncoder.getWidth(), numpy.uint8)
    consumptionBits = numpy.zeros(consumeEncoder.getWidth(), numpy.uint8)

    # fill encodings
    timeOfDayEncoder.encodeIntoArray(dateString, timeOfDayBits)
    weekendEncoder.encodeIntoArray(dateString, weekendBits)
    consumeEncoder.encodeIntoArray(consumption, consumptionBits)
    encoding = numpy.concatenate([timeOfDayBits, weekendBits, consumptionBits])

    #ONE = {'id': count, 'input': consumption, 'bucket': bucketIdx,
    #       'output': consumptionBits.tolist()}
    #print ONE
    #REZ.append(ONE)

    # spatial pooling
    activeColumns = numpy.zeros(COL_WIDTH, numpy.int8)
    sp.compute(encoding, True, activeColumns)
    activeColumnIndices = numpy.nonzero(activeColumns)[0]

    # temporal memory
    tm.compute(activeColumnIndices, learn=True)
    activeCells = tm.getActiveCells()

    # classification
    bucketIdx = consumeEncoder.getBucketIndices(consumption)[0]
    ###
    #hamming[bucketIdx] = consumptionBits
    ###
    classifierResult = classifier.compute(
      recordNum=count,
      patternNZ=activeCells,
      classification={"bucketIdx": bucketIdx,
                      "actValue": consumption},
      learn=True,
      infer=True)

    # prediction
    confidence, prediction = sorted(
      zip(classifierResult[1], classifierResult["actualValues"]),
      reverse=True)[0]

  #print json.dumps(REZ)

  # hamming distances
#  print("---")
#  keys = list(hamming.keys())
#  keys.sort()
#  bits = hamming[keys[100]]
#  prev = None
#  for i in range(len(keys)):
#    if prev is not None:
#      print "%s:\tprev=%s\tvalue=%s" % (i,
#         numpy.count_nonzero(prev != hamming[keys[i]]),
#         numpy.count_nonzero(bits != hamming[keys[i]]))
#    prev = hamming[keys[i]]

  # error stats
  errorNll = nll(consumptions, predictions)
  errorMae = mae(consumptions, predictions)
  errorMape = mape(consumptions, predictions)
  errorRmse = rmse(consumptions, predictions)
  print("---")
  print("mape: %s" % errorMape)
  print("mae: %s" % errorMae)
  print("rmse: %s" % errorRmse)
  print("nll_1000: %s" % errorNll)

