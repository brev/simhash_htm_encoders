// REQUIRES

const bitset = require('bitset')
const {floor} = Math
const hamming = require('compute-hamming')
const md5 = require('md5')
const {parseInt} = Number


// VARIABLES

const bit_size = 2**7 // md5 128-bit
const bucket_width = 7  // match exponent in bit_size..? even ok?
const bucket_half = floor(bucket_width / 2)
const simhash_threshold = 1  // raise for sparsity. simhash default 0 (~50%)
const values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
const query = process.argv[2]
let buckets = []
let hashes = []
let simhashes = []
let query_hash
let query_hash_string


// FUNCTIONS 

/**
 *
 */
function simhash_merge_hashes(hashes) {
  let weights = Array(hashes.length).fill(1)
  let sums = Array(hashes[0].length).fill(0)
  let results = sums.slice()
  // dynamic weights, favor center of bucket (value focus)
  for (i=0; i<=bucket_half; i++) {
    weights[i] = i + 1
    weights[weights.length - 1 - i] = i + 1
  }
  // simhash binary column sums/subs totals
  hashes.forEach((hash, hash_index) => {
    for(i=0; i<hash.length; i++) {
      if(hash[i] == '1') 
        sums[i] += 1 * weights[hash_index]
      else 
        sums[i] -= 1 * weights[hash_index]
    }
  })
  // convert sums back to binary
  sums.forEach((sum, sum_index) => {
    if(sum >= simhash_threshold) 
      results[sum_index] = 1
  })  
  /*
  console.log(
    'simhash % ',
    bitset.fromBinaryString(results.join('')).cardinality() / 
      hashes[0].length
  )
  */
  return results.join('')
}

/**
 *
 */
function hex_to_bit_string(hex) {
  return bitset.fromHexString(hex).toString().padStart(bit_size, '0')
}


// MAIN

// prep work on values
values.forEach((value, value_index) => {
  // fill md5 hash table of values
  hashes.push(md5(value))

  // create bucket groupings of value hashes - cyclical wrapping ON
  let bucket = []
  for (bucket_index=0; bucket_index<bucket_width; bucket_index++) {
    let relative_index = value_index - bucket_half + bucket_index
    // wrap array
    if (relative_index >= values.length) {
      relative_index -= values.length
    }
    else if (relative_index < 0) {
      relative_index += values.length
    }
    bucket.push(relative_index)
  }
  buckets.push(bucket)
})

console.log(hashes)
console.log(buckets)

// calculate simhashes for buckets
buckets.forEach((bucket, index) => {
  let hashes_buckets = []
  let simhash
  //console.log(`\n${index}`)
  bucket.forEach((hash_index) => {
    let bin = hex_to_bit_string(hashes[hash_index])
    hashes_buckets.push(bin) 
    //console.log(`  ${bin}`)
  })
  simhash = simhash_merge_hashes(hashes_buckets)
  //console.log(`  --------------------------------`)
  //console.log(`  ${simhash}`)
  simhashes.push(simhash)
})

// query value hash against simhash buckets
query_hash = hashes[query]
query_hash_string = hex_to_bit_string(query_hash)
console.log(`query:\n${query}\t${query_hash_string}\n`)
simhashes.forEach((simhash, index) => {
  let distance = hamming(query_hash_string, simhash)
  console.log(`${index}\t${simhash}\t${distance}`)
  //console.log(`\t`, hamming(simhashes[index], simhashes[index+1]))
})

