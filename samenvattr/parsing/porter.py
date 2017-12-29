#!/usr/bin/env python

"""Porter Stemming Algorithm
This is the Porter stemming algorithm, ported to Python from the
version coded up in ANSI C by the author. It may be be regarded
as canonical, in that it follows the algorithm presented in [1]_, see also [2]_

Author - Vivake Gupta (v@nano.com), optimizations and cleanup of the code by Lars Buitinck.

Examples:
---------
>>> from samenvattr.parsing.porter import PorterStemmer
>>>
>>> p = PorterStemmer()
>>> p.stem("apple")
'appl'
>>>
>>> p.stem_sentence("Cats and ponies have meeting")
'cat and poni have meet'
>>>
>>> p.stem_documents(["Cats and ponies", "have meeting"])
['cat and poni', 'have meet']

.. [1] Porter, 1980, An algorithm for suffix stripping, http://www.cs.odu.edu/~jbollen/IR04/readings/readings5.pdf
.. [2] http://www.tartarus.org/~martin/PorterStemmer

"""



class PorterStemmer(object):

    def __init__(self):
        from nltk.stem.snowball import DutchStemmer

        self.stemmer = DutchStemmer()

    def stem(self, w):
        """Stem the word `w`.

        Parameters
        ----------
        w : str

        Returns
        -------
        str
            Stemmed version of `w`.

        Examples
        --------
        >>> from samenvattr.parsing.porter import PorterStemmer
        >>> p = PorterStemmer()
        >>> p.stem("ponies")
        'poni'

        """
        w = w.lower()
        if len(w) <= 2:
            return w  # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        return self.stemmer.stem(w)

    def stem_sentence(self, txt):
        """Stem the sentence `txt`.

        Parameters
        ----------
        txt : str
            Input sentence.

        Returns
        -------
        str
            Stemmed sentence.

        Examples
        --------
        >>> from samenvattr.parsing.porter import PorterStemmer
        >>> p = PorterStemmer()
        >>> p.stem_sentence("Wow very nice woman with apple")
        'wow veri nice woman with appl'

        """
        return " ".join(self.stemmer.stem(x) for x in txt.split())

    def stem_documents(self, docs):
        """Stem documents.

        Parameters
        ----------
        docs : list of str
            Input documents

        Returns
        -------
        list of str
            Stemmed documents.

        Examples
        --------
        >>> from samenvattr.parsing.porter import PorterStemmer
        >>> p = PorterStemmer()
        >>> p.stem_documents(["Have a very nice weekend", "Have a very nice weekend"])
        ['have a veri nice weekend', 'have a veri nice weekend']

        """
        return [self.stem_sentence(x) for x in docs]


if __name__ == '__main__':
    import sys

    p = PorterStemmer()

    for f in sys.argv[1:]:
        with open(f) as infile:
            for line in infile:
                print(p.stem_sentence(line))
