Inital Research Repository. Most recent code should be with [NuPIC][nupic].


### SimHash Distributed Scalar Encoder (SHaDSE)

A [Locality-Sensitive Hashing][lsh] approach towards encoding semantic data
into [Sparse Distributed Representations][sdr], ready to be fed into an
[Hierarchical Temporal Memory][htm], like [NuPIC][nupic] by
[Numenta][numenta]. This uses the [SimHash][simhash] algorithm to accomplish
this.

This encoder is sibling with the original [Scalar Encoder][scalar], and the
[Random Distributed Scalar Encoder][rdse] (RDSE). The static bucketing
strategy here is generally lifted straight from the RDSE, although the
"contents" and representations are created differently.

Instead of creating a random hash for our target bucket, we first generate a
[SHA-3+SHAKE256][sha3] hash of the bucket index (the SHAKE extension provides
a variable-length hash (n)). Using that hash, and hash values from nearby
neighbor buckets (within bucketRadius), we then create a weighted SimHash for
our target bucket index. This SimHash output will represent both individual
bucket value, and represent the relations between nearby neighbor values in
bucket space. A stable number of On bits (w) is achieved during final
collapsing step of SimHashing.

More Information:
* [HTM Community Discussion][disc]
* [Origial Article about SHaDSE][perma]


[disc]: https://discourse.numenta.org/t/new-simhash-distributed-scalar-encoder-shadse/5860
[htm]: https://numenta.com/machine-intelligence-technology/
[lsh]: https://en.wikipedia.org/wiki/Locality-sensitive_hashing
[numenta]: https://numenta.com
[nupic]: https://github.com/numenta/nupic
[perma]: http://www.luxrota.com/articles/2019/04/18/simhash-distributed-scalar-encoder-for-htm.html
[rdse]: https://github.com/numenta/nupic/blob/master/src/nupic/encoders/random_distributed_scalar.py
[scalar]: https://github.com/numenta/nupic/blob/master/src/nupic/encoders/scalar.py
[sdr]: https://numenta.com/neuroscience-research/sparse-distributed-representations/
[sha3]: https://en.wikipedia.org/wiki/SHA-3
[simhash]: https://en.wikipedia.org/wiki/SimHash

