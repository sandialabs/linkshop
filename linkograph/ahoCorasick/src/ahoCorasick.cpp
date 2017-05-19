#include <queue>
#include <string.h>
#include "ahoCorasick.h"

// Microsoft's standard functions aren't safe rampages suck
#define CRT_SECURE_NO_WARNINGS

// Queue use to create AC failure function
typedef std::queue<trieIndex> stateQueue;

static inline alphabetPresence getAlphabetSize(wordChars * words[], trieIndex numWords)
{
    // Bitset to indicate occurence or non-occurance of characters in the trie corpus
    alphabetPresence alphabet;

    // Find all the characters used in the trie corpus
    for (defaultIndex i = 0; i < numWords; ++i)
    {
        wordChars * wordPtr = words[i];
        defaultIndex j = 0;

        while (wordPtr[j])
        {
            alphabet[wordPtr[j]] = 1;
            ++j;
        }
    }

    return alphabet;
}

static inline charIndexMap buildIndexMap(alphabetPresence& alphabet)
{
    // Array used to find the index of characters in the alphabet
    charIndexMap indexMap;

    // Build the array
    defaultIndex currentIndex = 0;
    for (defaultIndex i = 0; i < 256; ++i)
    {
        if (alphabet.test(i))
        {
            indexMap.indexes[i] = currentIndex;
            ++currentIndex;
        }
        else
        {
            indexMap.indexes[i] = NOT_ASSIGNED;
        }
    }

    return indexMap;
}

void buildTrie(wordChars * words[], trieIndex numWords, trieData& finalTrie)
{
    if (numWords >= NOT_ASSIGNED)
    {
        throw TOO_MANY_WORDS;
    }

    // Building a list of actually used charaters reduces memory usage
    alphabetPresence alphabet    = getAlphabetSize(words, numWords);

    charIndexMap indexMap        = buildIndexMap(alphabet);

    defaultSize alphabetSize     = (defaultSize) alphabet.count();

    // Allocate trie
    indexArray trie(alphabetSize, NOT_ASSIGNED);

    // Allocate output
    outputOfState stateOutputs(1);

    // Keep track of the number of states
    trieIndex states = 1, prevWordState = 1;

    // Add each word to the tree
    for (defaultIndex i = 0; i < numWords; ++i)
    {
        defaultIndex j = 0, currentState = 0;
        wordChars * wordPtr = words[i];

        while (wordPtr[j])
        {
            trieIndex index = currentState * alphabetSize + indexMap.indexes[wordPtr[j]];

            if (trie[index] == NOT_ASSIGNED)
            {
                // Create new state
                trie[index] =  states++;
                if(states >= NOT_ASSIGNED)
                {
                    throw STATE_OVERFLOW;
                }
                trie.resize(states * alphabetSize, NOT_ASSIGNED);
            }
            currentState = trie[index];
            j++;
        }

        // Set ouput entry when end of the word is reached
        if (states != prevWordState)
        {
            stateOutputs.resize(states);
            prevWordState = states;
        }
        stateOutputs[currentState].push_back(i);
    }

    indexArray failureFunc(states, NOT_ASSIGNED);
    stateQueue q;

    // Initialize failure function
    for (defaultIndex i = 0; i < alphabetSize; ++i)
    {
        if (trie[i] == NOT_ASSIGNED) trie[i] = 0;
        else
        {
            failureFunc[trie[i]] = 0;
            q.push(trie[i]);
        }
    }

    // Build failure function
    while (q.size())
    {
        trieIndex currentState = q.front();
        q.pop();

        // Build failure function each of the next states
        for (defaultIndex i = 0; i < alphabetSize; ++i)
        {
            trieIndex index = currentState * alphabetSize + i;

            if (trie[index] != NOT_ASSIGNED)
            {
                trieIndex failure = failureFunc[currentState];

                // Find longest suffix in trie
                while (trie[failure * alphabetSize + i] == NOT_ASSIGNED)
                {
                    failure = failureFunc[failure];
                }
                failure = trie[failure * alphabetSize + i];
                failureFunc[trie[index]] = failure;

                // Copy outputs from failure
                stateOutputs[trie[index]].insert(stateOutputs[trie[index]].end(), stateOutputs[failure].begin(), stateOutputs[failure].end());

                q.push(trie[index]);
            }
        }
    }

    // Shrink dynamic arrays to fit actual size of allocated objects (swap trick)
    indexArray(trie).swap(trie);
    indexArray(failureFunc).swap(failureFunc);
    outputOfState(stateOutputs).swap(stateOutputs);

    // Populate final trie structure
    finalTrie.alphabetSize = alphabetSize;
    finalTrie.numWords     = numWords;
    memcpy(finalTrie.indexMap.indexes, indexMap.indexes, 256 * sizeof(defaultIndex));
    finalTrie.trie.swap(trie);
    finalTrie.failureFunc.swap(failureFunc);
    finalTrie.outputs.swap(stateOutputs);
}

static inline trieIndex findNextState(trieIndex currentState, wordChars nextChar, trieData& trie)
{
    trieIndex answer       = currentState;
    defaultIndex charIndex = trie.indexMap.indexes[nextChar];

    // If character is not in the set of used characters in the substring corpus go to 0
    if (charIndex == NOT_ASSIGNED)
    {
        return 0;
    }

    // If failure, go to failure state
    while (trie.trie[answer * trie.alphabetSize + charIndex] == NOT_ASSIGNED)
    {
        answer = trie.failureFunc[answer];
    }

    return trie.trie[answer * trie.alphabetSize + charIndex];
}

matches searchString(wordChars searchString [], trieData& trie)
{
    defaultIndex i = 0;
    trieIndex currentState = 0;

    matches results;

    // Walk trie and search searchString
    while (searchString[i])
    {
        currentState = findNextState(currentState, searchString[i], trie);

        // At each state ouput any substrings that are found
        if (trie.outputs[currentState].size() > 0)
        {
            for (outputList::iterator iter = trie.outputs[currentState].begin(); iter != trie.outputs[currentState].end(); ++iter)
            {
                results.push_front(matchObj(*iter,i));
            }
        }
        i++;
    }
    return results;
}
