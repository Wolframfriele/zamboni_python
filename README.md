# Zamboni

This tool is a terminal based autocorrect prototype. The goal is to test out different methods of setting up autocorrection, with the goal of typing faster and learning about spelling checking / correction.

# Options

1. No correction, just typing in words, explaining how to set up text input in the terminal.
2. Only checking if the word exists, maybe the word get's a different color when it's not in a list?
3. Edit distance based optimization, looking at the edit distance to words when the input is not in the dictionary
4. Edit distance + word frequency, allow more common words to score higher
5. Context aware: Add a markov chain that uses the previous word to have likely next words, include word frequency for the combinations

# Structure

A terminal editor that you can swap out different methods of checking spelling, maybe the logical level is to make an interface for a text buffer, and just swap out entire text buffers. 


# Markov Chain

For the markov chain lookup speed and storage size need to be balanced. This requires a good way to find words, but also not use strings for everything to avoid duplicating words. 
Steps in looking up corrections:


1. Check if current word is in potential words


## Examples

Sample sentence: all the time new things

Option 1:

Using a list for the words, using the indexes in a dictionary.

words = ["all", "the", "time", "new", "things"]
bigram = {0: [1], 1: [2, 3, 4], 2: [3]}

Relatively space efficient, but the problem is that looking up words is slow since the the list can not be sorted.

Option 2:

Using a dictionary for everything:

{
    "all": ["the"],
    "the": ["time", "new", "things"],
    "time": ["new"],
    "new": ["things"],
    "things": [],
}

Would work but takes quite a bit of space, would need to check how much actual space it takes.

# Training data

[1 billion word corpus](https://www.statmt.org/lm-benchmark/)
