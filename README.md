# SAMENVATTR

Dutch-language extractive text summarization tool. Almost everything was ripped out of Gensim's amazing English language extractive summarization tool; they deserve the lion's share of the credit and you can visit the relevant doc from their API [here](https://radimrehurek.com/gensim/summarization/summariser.html).

# How do I use it?

```python
from samenvattr import summarize

article = "...some text..."
summarize(article, word_count=100)
```

Of course, you can use a word count of your choice. What's returned are the most important sentences, in order, concatenated with a newline in between. It's a bit sensitive to whitespace characters, so it's a good idea to run your `article` through this function first before passing it to `summarize`:

```python
def preprocess_text(text):
    import re
    text = re.sub(r'\n|\r|\t', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text
```

# What exactly did you do, then?

There are a few important changes:

+ this is Python 3-only
+ the English lemmatizer from Pattern was swapped out with the Dutch version in Pattern3
+ the English stopword list was swapped out with a Dutch list; my source was [Stopwords ISO](https://github.com/stopwords-iso/stopwords-nl)
+ the English Porter stemmer was swapped out with nltk's [Dutch snowball stemmer](http://www.nltk.org/_modules/nltk/stem/snowball.html#DutchStemmer)
+ most code and tests relating to non-summarization corners of the API were ripped out

# What are you still looking to do?

+ rip out all of the functionality that doesn't relate to summarization
+ evaluate whether the sentence segmentation and abbreviation regexes in `utils.py` are sufficient for Dutch, and if not look at spaCy-based solutions 
+ go over the code again to make sure there aren't any unnecessary Python 2-compatibility checks
+ I just realized that all of the tests assume the input is English, so I'll have to come up with some Dutch test data
