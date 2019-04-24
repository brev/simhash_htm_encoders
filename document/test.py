import numpy

from simhash_distributed_document import SimHashDistributedDocumentEncoder


# setup

encoder = SimHashDistributedDocumentEncoder(
  n=400,
  w=21,
  verbosity=3)

encodingWidth = (encoder.getWidth())

### non-weighted
#documents = [
#  ['apples', 'age', 'well', 'in', 'the', 'sun'],
#  ['sun', 'valley', 'apples', 'well', 'the', 'best'],
#  ['best', 'age', 'to', 'travel', 'is', 'young'],
#  ['travel', 'young', 'toward', 'the', 'sun'],
#  ['travel', 'with', 'a', 'wild', 'rowdy', 'bunch'],
#  ['my', 'brain', 'hates', 'creating', 'examples'],
#]

### weighted
documents = [
  {'apples':3, 'age':2, 'well':3, 'in':2, 'the':1, 'sun':3},
  {'sun':3, 'valley':3, 'apples':3, 'well':2, 'the':1, 'best':2},
  {'best':2, 'age':2, 'to':2, 'travel':3, 'is':1, 'young':3},
  {'travel':3, 'young':2, 'toward':3, 'the':1, 'sun':3},
  {'travel':3, 'with':1, 'a':1, 'wild':3, 'rowdy':3, 'bunch':3},
  {'my':1, 'brain':3, 'hates':3, 'creating':3, 'examples':3},
]


# MAIN

encodings = []

for count in range(len(documents)):
  document = documents[count]
  encodingBits = numpy.zeros(encoder.getWidth(), numpy.uint8)
  encoder.encodeIntoArray(document, encodingBits)
  encoding = encodingBits
  encodings.append(encoding)

for outer, document in list(enumerate(documents)):
  print "%s\t%s" % (outer, document)
  for inner, document in list(enumerate(documents)):
    print "\t%s\t%s\t%s" % (inner,
        numpy.count_nonzero(encodings[outer] != encodings[inner]),
        document)

