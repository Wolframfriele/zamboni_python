# Zamboni

This tool is a terminal based autocorrect prototype. The goal is to test out different methods of setting up autocorrection, with the goal of typing faster and learning about spelling checking / correction.

The prototype runs on curses, and needs the `windows-curses` library on windows. 

# Structure

There are some exercises you can make in the mini_projects. The folder 1_no_auto_correct, contains a blank template to have basic terminal text editor functionality, you can use this to build spelling correct into. The folder 2_single_word has autocorrect based on the edit distance to a word in a dictionary. Lastly the folder 3_context_aware contains the setup to use a markov model to improve the autocorrection.

# Spelling Correct

A good [wordlist](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt) to use to check words against.

# Markov Chain

The markov chain can be trained on any corpus, an example of a pre tokenized dataset is the [1 billion word corpus](https://www.statmt.org/lm-benchmark/).
If you want to use a different text, it can easily be tokenized with the [NLTK Tokenizer package](https://www.nltk.org/api/nltk.tokenize.html), this functionality is not build in, but can easily be added. Look into `3_context_aware/buffer/markov_model.py` in the Markov class the `.split()` in the `_load_corpus` method can be replaced with NLTK `word_tokenize`.

