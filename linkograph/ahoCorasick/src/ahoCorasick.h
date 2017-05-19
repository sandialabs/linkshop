#ifndef AHOCORASICK_H
#define AHOCORASICK_H

#include <climits>
#include <stdexcept>

// Containers
#include <list>
#include <utility>
#include <bitset>
#include <vector>

// Package specific error for overflow exceptions
#define TOO_MANY_WORDS (std::invalid_argument("Number of words is too large"))
#define STATE_OVERFLOW (std::overflow_error("Too many states for trie to handle"))

// -----------------------------------------------------------------------------
/**
    Implementation of the Aho-Corasick algorithm for efficient substring matching.
    Use of dynamic STL containters and minimum alphabet size reduces memory usage.
*/
// -----------------------------------------------------------------------------

// Symbols making up trie substrings that are used to index character maps
typedef unsigned char wordChars;

// Make sure the trie states are indexed with integer values that are at least
// 4 bytes in length
#if UINT_MAX < 4294967295

    // Distinguish default index and size types from trie state indexes
    typedef unsigned long defaultIndex;
    typedef defaultIndex defaultSize;

    // Datatype used for trie
    typedef unsigned long trieIndex;

    // Value to indicate index is not set
    static const trieIndex NOT_ASSIGNED = ULONG_MAX;

#else

    // Distinguish default index and size types from trie state indexes
    typedef unsigned int defaultIndex;
    typedef defaultIndex defaultSize;

    // Datatype used for trie
    typedef unsigned int trieIndex;

    // Value to indicate index is not set
    static const trieIndex NOT_ASSIGNED = UINT_MAX;


#endif

// Static bitset used to indicate alphabet membership in a corpus of substrings
typedef std::bitset<256> alphabetPresence;

// Used for trie and failure function
typedef std::vector<trieIndex> indexArray;

// Used for state output
typedef std::list<trieIndex> outputList;
typedef std::vector<outputList> outputOfState;

// Represents a match of substring with index "first" at index of "second" in a query
typedef std::pair<defaultIndex, defaultIndex> matchObj;

// All such matches for a given query
typedef std::list<matchObj> matches;

// Array used to find the index of a particular character on a given node of the trie
typedef struct array256
{
    defaultIndex indexes[256];
} charIndexMap;

// Final datastructure used to hold a built trie
typedef struct builtTrie
{
     defaultSize   alphabetSize;
     defaultSize   numWords;
     charIndexMap  indexMap;
     indexArray    trie;
     indexArray    failureFunc;
     outputOfState outputs;
} trieData;

// Get all the characters used in a corpus of substrings
static inline alphabetPresence getAlphabetSize(wordChars * words[], trieIndex numWords);

// Create an array mapping all possible charaters to their corresponding indexes
static inline charIndexMap buildIndexMap(alphabetPresence& alphabet);

// Actually create the trie with failure function and outputs
void buildTrie(wordChars * words[], trieIndex numWords, trieData& finalTrie);

// Function to walk the trie
static inline trieIndex findNextState(trieIndex currentState, wordChars nextChar, trieData& trie);

// Query the trie for all substrings that are present in the searchString
matches searchString(wordChars searchString [], trieData& trie);

#endif // AHOCORASICK_H
