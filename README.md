# SAMENVATTR

Dutch-language extractive text summarization tool. Almost everything was ripped out of Gensim's amazing English language extractive summarization tool; they deserve the lion's share of the credit and you can visit the relevant doc from their API [here](https://radimrehurek.com/gensim/summarization/summariser.html).

# What exactly did you do, then?

There are a few important changes:

+ this is Python 3-only
+ the English lemmatizer from Pattern was swapped out with the Dutch version in Pattern3
+ the English stopword list was swapped out with a Dutch list; my source was [Stopwords ISO](https://github.com/stopwords-iso/stopwords-nl)
+ the English Porter stemmer was swapped out with nltk's [Dutch snowball stemmer](http://www.nltk.org/_modules/nltk/stem/snowball.html#DutchStemmer)
+ most code and tests relating to non-summarization corners of the API were ripped out

