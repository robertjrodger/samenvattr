#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""This module contains methods for parsing and preprocessing strings. Let's consider the most noticeable:

* :func:`~samenvattr.parsing.preprocessing.remove_stopwords` - remove all stopwords from string
* :func:`~samenvattr.parsing.preprocessing.preprocess_string` -  preprocess string (in default NLP meaning)

Examples:
---------
>>> from samenvattr.parsing.preprocessing import remove_stopwords
>>> remove_stopwords("Better late than never, but better never late.")
u'Better late never, better late.'
>>>
>>> preprocess_string("<i>Hel 9lo</i> <b>Wo9 rld</b>! Th3     weather_is really g00d today, isn't it?")
[u'hel', u'rld', u'weather', u'todai', u'isn']


Data:
-----

.. data:: STOPWORDS - Set of stopwords from Stone, Denis, Kwantes (2010).
.. data:: RE_PUNCT - Regexp for search an punctuation.
.. data:: RE_TAGS - Regexp for search an tags.
.. data:: RE_NUMERIC - Regexp for search an numbers.
.. data:: RE_NONALPHA - Regexp for search an non-alphabetic character.
.. data:: RE_AL_NUM - Regexp for search a position between letters and digits.
.. data:: RE_NUM_AL - Regexp for search a position between digits and letters .
.. data:: RE_WHITESPACE - Regexp for search space characters.
.. data:: DEFAULT_FILTERS - List of function for string preprocessing.

"""

import re
import string
import glob

from samenvattr import utils
from samenvattr.parsing.porter import PorterStemmer


STOPWORDS = frozenset([
    'aan','aangaande', 'aangezien', 'achte', 'achter', 'achterna', 'af', 'afgelopen', 'al', 'aldaar', 'aldus',
    'alhoewel', 'alias', 'alle', 'allebei', 'alleen', 'alles', 'als', 'alsnog', 'altijd', 'altoos', 'ander', 'andere',
    'anders', 'anderszins', 'beetje', 'behalve', 'behoudens', 'beide', 'beiden', 'ben', 'beneden', 'bent', 'bepaald',
    'betreffende', 'bij', 'bijna', 'bijv', 'binnen', 'binnenin', 'blijkbaar', 'blijken', 'boven', 'bovenal',
    'bovendien', 'bovengenoemd', 'bovenstaand', 'bovenvermeld', 'buiten', 'bv', 'daar', 'daardoor', 'daarheen',
    'daarin', 'daarna', 'daarnet', 'daarom', 'daarop', 'daaruit', 'daarvanlangs', 'dan', 'dat', 'de', 'deden', 'deed',
    'der', 'derde', 'derhalve', 'dertig', 'deze', 'dhr', 'die', 'dikwijls', 'dit', 'doch', 'doe', 'doen', 'doet',
    'door', 'doorgaand', 'drie', 'duizend', 'dus', 'echter', 'een', 'eens', 'eer', 'eerdat', 'eerder', 'eerlang',
    'eerst', 'eerste', 'eigen', 'eigenlijk', 'elk', 'elke', 'en', 'enig', 'enige', 'enigszins', 'enkel', 'er', 'erdoor',
    'erg', 'ergens', 'etc', 'etcetera', 'even', 'eveneens', 'evenwel', 'gauw', 'ge', 'gedurende', 'geen', 'gehad',
    'gekund', 'geleden', 'gelijk', 'gemoeten', 'gemogen', 'genoeg', 'geweest', 'gewoon', 'gewoonweg', 'haar',
    'haarzelf', 'had', 'hadden', 'hare', 'heb', 'hebben', 'hebt', 'hedden', 'heeft', 'heel', 'hem', 'hemzelf', 'hen',
    'het', 'hetzelfde', 'hier', 'hierbeneden', 'hierboven', 'hierin', 'hierna', 'hierom', 'hij', 'hijzelf', 'hoe',
    'hoewel', 'honderd', 'hun', 'hunne', 'ieder', 'iedere', 'iedereen', 'iemand', 'iets', 'ik', 'ikzelf', 'in',
    'inderdaad', 'inmiddels', 'intussen', 'inzake', 'is', 'ja', 'je', 'jezelf', 'jij', 'jijzelf', 'jou', 'jouw',
    'jouwe', 'juist', 'jullie', 'kan', 'klaar', 'kon', 'konden', 'krachtens', 'kun', 'kunnen', 'kunt', 'laatst',
    'later', 'liever', 'lijken', 'lijkt', 'maak', 'maakt', 'maakte', 'maakten', 'maar', 'mag', 'maken', 'me', 'meer',
    'meest', 'meestal', 'men', 'met', 'mevr', 'mezelf', 'mij', 'mijn', 'mijnent', 'mijner', 'mijzelf', 'minder', 'miss',
    'misschien', 'missen', 'mits', 'mocht', 'mochten', 'moest', 'moesten', 'moet', 'moeten', 'mogen', 'mr', 'mrs', 'mw',
    'na', 'naar', 'nadat', 'nam', 'namelijk', 'nee', 'neem', 'negen', 'nemen', 'nergens', 'net', 'niemand', 'niet',
    'niets', 'niks', 'noch', 'nochtans', 'nog', 'nogal', 'nooit', 'nu', 'nv', 'of', 'ofschoon', 'om', 'omdat', 'omhoog',
    'omlaag', 'omstreeks', 'omtrent', 'omver', 'ondanks', 'onder', 'ondertussen', 'ongeveer', 'ons', 'onszelf', 'onze',
    'onzeker', 'ooit', 'ook', 'op', 'opnieuw', 'opzij', 'over', 'overal', 'overeind', 'overige', 'overigens', 'paar',
    'pas', 'per', 'precies', 'recent', 'redelijk', 'reeds', 'rond', 'rondom', 'samen', 'sedert', 'sinds', 'sindsdien',
    'slechts', 'sommige', 'spoedig', 'steeds', 'tamelijk', 'te', 'tegen', 'tegenover', 'tenzij', 'terwijl', 'thans',
    'tien', 'tiende', 'tijdens', 'tja', 'toch', 'toe', 'toen', 'toenmaals', 'toenmalig', 'tot', 'totdat', 'tussen',
    'twee', 'tweede', 'u', 'uit', 'uitgezonderd', 'uw', 'vaak', 'vaakwat', 'van', 'vanaf', 'vandaan', 'vanuit',
    'vanwege', 'veel', 'veeleer', 'veertig', 'verder', 'verscheidene', 'verschillende', 'vervolgens', 'via', 'vier',
    'vierde', 'vijf', 'vijfde', 'vijftig', 'vol', 'volgend', 'volgens', 'voor', 'vooraf', 'vooral', 'vooralsnog',
    'voorbij', 'voordat', 'voordezen', 'voordien', 'voorheen', 'voorop', 'voorts', 'vooruit', 'vrij', 'vroeg', 'waar',
    'waarom', 'waarschijnlijk', 'wanneer', 'want', 'waren', 'was', 'wat', 'we', 'wederom', 'weer', 'weg', 'wegens',
    'weinig', 'wel', 'weldra', 'welk', 'welke', 'werd', 'werden', 'werder', 'wezen', 'whatever', 'wie', 'wiens', 'wier',
    'wij', 'wijzelf', 'wil', 'wilden', 'willen', 'word', 'worden', 'wordt', 'zal', 'ze', 'zei', 'zeker', 'zelf',
    'zelfde', 'zelfs', 'zes', 'zeven', 'zich', 'zichzelf', 'zij', 'zijn', 'zijne', 'zijzelf', 'zo', 'zoals', 'zodat',
    'zodra', 'zonder', 'zou', 'zouden', 'zowat', 'zulk', 'zulke', 'zullen', 'zult'
])


RE_PUNCT = re.compile(r'([%s])+' % re.escape(string.punctuation), re.UNICODE)
RE_TAGS = re.compile(r"<([^>]+)>", re.UNICODE)
RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)
RE_NONALPHA = re.compile(r"\W", re.UNICODE)
RE_AL_NUM = re.compile(r"([a-z]+)([0-9]+)", flags=re.UNICODE)
RE_NUM_AL = re.compile(r"([0-9]+)([a-z]+)", flags=re.UNICODE)
RE_WHITESPACE = re.compile(r"(\s)+", re.UNICODE)


def remove_stopwords(s):
    """Remove :const:`~samenvattr.parsing.preprocessing.STOPWORDS` from `s`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string without :const:`~samenvattr.parsing.preprocessing.STOPWORDS`.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import remove_stopwords
    >>> remove_stopwords("Better late than never, but better never late.")
    u'Better late never, better late.'

    """
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in STOPWORDS)


def strip_punctuation(s):
    """Replace punctuation characters with spaces in `s` using :const:`~samenvattr.parsing.preprocessing.RE_PUNCT`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string without punctuation characters.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import strip_punctuation
    >>> strip_punctuation("A semicolon is a stronger break than a comma, but not as much as a full stop!")
    u'A semicolon is a stronger break than a comma  but not as much as a full stop '

    """
    s = utils.to_unicode(s)
    return RE_PUNCT.sub(" ", s)


strip_punctuation2 = strip_punctuation


def strip_tags(s):
    """Remove tags from `s` using :const:`~samenvattr.parsing.preprocessing.RE_TAGS`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string without tags.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import strip_tags
    >>> strip_tags("<i>Hello</i> <b>World</b>!")
    u'Hello World!'

    """
    s = utils.to_unicode(s)
    return RE_TAGS.sub("", s)


def strip_short(s, minsize=3):
    """Remove words with length lesser than `minsize` from `s`.

    Parameters
    ----------
    s : str
    minsize : int, optional

    Returns
    -------
    str
        Unicode string without short words.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import strip_short
    >>> strip_short("salut les amis du 59")
    u'salut les amis'
    >>>
    >>> strip_short("one two three four five six seven eight nine ten", minsize=5)
    u'three seven eight'

    """
    s = utils.to_unicode(s)
    return " ".join(e for e in s.split() if len(e) >= minsize)


def strip_numeric(s):
    """Remove digits from `s` using :const:`~samenvattr.parsing.preprocessing.RE_NUMERIC`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode  string without digits.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import strip_numeric
    >>> strip_numeric("0text24samenvattr365test")
    u'textsamenvattrtest'

    """
    s = utils.to_unicode(s)
    return RE_NUMERIC.sub("", s)


def strip_non_alphanum(s):
    """Remove non-alphabetic characters from `s` using :const:`~samenvattr.parsing.preprocessing.RE_NONALPHA`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string with alphabetic characters only.

    Notes
    -----
    Word characters - alphanumeric & underscore.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import strip_non_alphanum
    >>> strip_non_alphanum("if-you#can%read$this&then@this#method^works")
    u'if you can read this then this method works'

    """
    s = utils.to_unicode(s)
    return RE_NONALPHA.sub(" ", s)


def strip_multiple_whitespaces(s):
    r"""Remove repeating whitespace characters (spaces, tabs, line breaks) from `s`
    and turns tabs & line breaks into spaces using :const:`~samenvattr.parsing.preprocessing.RE_WHITESPACE`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string without repeating in a row whitespace characters.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import strip_multiple_whitespaces
    >>> strip_multiple_whitespaces("salut" + '\r' + " les" + '\n' + "         loulous!")
    u'salut les loulous!'

    """
    s = utils.to_unicode(s)
    return RE_WHITESPACE.sub(" ", s)


def split_alphanum(s):
    """Add spaces between digits & letters in `s` using :const:`~samenvattr.parsing.preprocessing.RE_AL_NUM`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string with spaces between digits & letters.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import split_alphanum
    >>> split_alphanum("24.0hours7 days365 a1b2c3")
    u'24.0 hours 7 days 365 a 1 b 2 c 3'

    """
    s = utils.to_unicode(s)
    s = RE_AL_NUM.sub(r"\1 \2", s)
    return RE_NUM_AL.sub(r"\1 \2", s)


def stem_text(text):
    """Transform `s` into lowercase and stem it.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        Unicode lowercased and porter-stemmed version of string `text`.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import stem_text
    >>> stem_text("While it is quite useful to be able to search a large collection of documents almost instantly.")
    u'while it is quit us to be abl to search a larg collect of document almost instantly.'

    """
    text = utils.to_unicode(text)
    p = PorterStemmer()
    return ' '.join(p.stem(word) for word in text.split())


stem = stem_text


DEFAULT_FILTERS = [
    lambda x: x.lower(), strip_tags, strip_punctuation,
    strip_multiple_whitespaces, strip_numeric,
    remove_stopwords, strip_short, stem_text
]


def preprocess_string(s, filters=DEFAULT_FILTERS):
    """Apply list of chosen filters to `s`.

    Default list of filters:

    * :func:`~samenvattr.parsing.preprocessing.strip_tags`,
    * :func:`~samenvattr.parsing.preprocessing.strip_punctuation`,
    * :func:`~samenvattr.parsing.preprocessing.strip_multiple_whitespaces`,
    * :func:`~samenvattr.parsing.preprocessing.strip_numeric`,
    * :func:`~samenvattr.parsing.preprocessing.remove_stopwords`,
    * :func:`~samenvattr.parsing.preprocessing.strip_short`,
    * :func:`~samenvattr.parsing.preprocessing.stem_text`.

    Parameters
    ----------
    s : str
    filters: list of functions, optional

    Returns
    -------
    list of str
        Processed strings (cleaned).

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import preprocess_string
    >>> preprocess_string("<i>Hel 9lo</i> <b>Wo9 rld</b>! Th3     weather_is really g00d today, isn't it?")
    [u'hel', u'rld', u'weather', u'todai', u'isn']
    >>>
    >>> s = "<i>Hel 9lo</i> <b>Wo9 rld</b>! Th3     weather_is really g00d today, isn't it?"
    >>> CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation]
    >>> preprocess_string(s, CUSTOM_FILTERS)
    [u'hel', u'9lo', u'wo9', u'rld', u'th3', u'weather', u'is', u'really', u'g00d', u'today', u'isn', u't', u'it']

    """
    s = utils.to_unicode(s)
    for f in filters:
        s = f(s)
    return s.split()


def preprocess_documents(docs):
    """Apply :const:`~samenvattr.parsing.preprocessing.DEFAULT_FILTERS` to the documents strings.

    Parameters
    ----------
    docs : list of str

    Returns
    -------
    list of list of str
        Processed documents split by whitespace.

    Examples
    --------
    >>> from samenvattr.parsing.preprocessing import preprocess_documents
    >>> preprocess_documents(["<i>Hel 9lo</i> <b>Wo9 rld</b>!", "Th3     weather_is really g00d today, isn't it?"])
    [[u'hel', u'rld'], [u'weather', u'todai', u'isn']]

    """
    return [preprocess_string(d) for d in docs]


def read_file(path):
    with utils.smart_open(path) as fin:
        return fin.read()


def read_files(pattern):
    return [read_file(fname) for fname in glob.glob(pattern)]
