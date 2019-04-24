Inital Research Repository. Most recent code should be with [NuPIC][nupic].


## SimHash Distributed Document Encoder (SHaDDE)

Using the same approch as the recent [SimHash Scalar Encoder][lvxshadse], there
is now a version available which can encode **Documents**.

This also uses a [Locality-Sensitive Hashing][lsh] approach towards encoding
semantic document text data into [Sparse Distributed Representations][sdr],
ready to be fed into an [Hierarchical Temporal Memory][htm], like
[NuPIC][nupic] by [Numenta][numenta]. This uses the [SimHash][simhash]
algorithm to accomplish this. LSH and SimHash come from the world of
nearest-neighbor document similarity searching.

Document Tokens are supplied with opitional weighting values. We generate a
SHA-3 hash digest for each word token (using SHAKE256 to get a variable-width
digest output size). The hashes for a document are combined into a sparse
SimHash. Documents that are semantically similar will have similar encodings.
Dissimilar documents will have very different encodings from each other.
Similarity is defined as binary distance between strings, there is no kind of
linguistic semantic understanding.  You'll want http://cortical.io for that.

### How It Works

* Take a document, split up the words, and hash each.
* You can optionally add weights to the word hashes of your document.
* Combine the hashes into a sparse SimHash for the document
  (same method as [SimHash Scalar encoder][discshadse]).

### Source Code

* [Pull Request against Old NuPIC][pr].
* [Research Repo][repo] with my test runners and original research code.

### Next Steps

* Change each word from being a hash, to being a simhash created from the
  hashes of each letter in the word. This way, near-spellings will be
  considered similar ("eat" vs. "eats"), which they currently are not.

### More Information

* [HTM Community Discussion][disc]
* [Origial Article][perma]

[disc]: https://discourse.numenta.org/t/also-simhash-document-encoder/5893
[discshadse]: https://discourse.numenta.org/t/new-simhash-distributed-scalar-encoder-shadse/5860
[htm]: https://numenta.com/machine-intelligence-technology/
[lsh]: https://en.wikipedia.org/wiki/Locality-sensitive_hashing
[lvxshadse]: https://www.luxrota.com/articles/2019/04/18/simhash-distributed-scalar-encoder-for-htm.html
[numenta]: https://numenta.com
[nupic]: https://github.com/numenta/nupic
[perma]: https://www.luxrota.com/articles/2019/04/23/simhash-distributed-document-encoder-for-htm.html
[pr]: https://github.com/numenta/nupic/pull/3872
[repo]: https://github.com/luxrota/simhash_htm_encoders
[sdr]: https://numenta.com/neuroscience-research/sparse-distributed-representations/
[simhash]: https://en.wikipedia.org/wiki/SimHash

