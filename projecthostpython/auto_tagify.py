import re
import urllib

import nltk

from nltk.stem.wordnet import WordNetLemmatizer

#CLEAN_LINK = re.compile('(?<=^\/)\/+|\/+$')
CLEAN_WORD = re.compile('[\[\],().:;"\/\'?*%!*+=@$;#%{}`~\r\n\t]')
LONG_DASH = re.compile('(\&#8212;)')
MIN_TAG_LENGTH = 3
MAX_TAG_LENGTH = 15
SMART_QUOTES_D = re.compile('(\xe2\x80\x9c)|(\xe2\x80\x9d)|(\&#8220;)|(\&#8221;)')
SMART_QUOTES_S = re.compile('(\xe2\x80\x98)|(\xe2\x80\x99)|(\&#8216;)|(\&#8217;)')
STOP_WORDS = ['DT', 'IN', 'TO', 'VBD', 'VBD', 'VBG', 'VBN', 'VBZ', 'MD', 'RB',
              'CC', 'WDT', 'PRO', 'PRP', 'PRP$']


class AutoTagify():
    lemma = WordNetLemmatizer()

    def __init__(self):
        self.text = ''

    def _tokenize(self):
        """Tag words from the string."""
        return nltk.pos_tag(nltk.word_tokenize(self._clean_text()))

    def _cleaned(self, word, strict):
        lemmatized = self.lemma.lemmatize(self._clean_text(word))
        if strict:
            return lemmatized
        else:
            return urllib.parse.quote(self._clean_text(word))

    def _clean_text(self, word=''):
        if len(word) > MIN_TAG_LENGTH:
            return CLEAN_WORD.sub('', self._replace_special_chars(word.lower()))
        else:
            return CLEAN_WORD.sub('', self._replace_special_chars(self.text))

    def _replace_special_chars(self, text):
        return SMART_QUOTES_S.sub('\'', SMART_QUOTES_D.sub('"', LONG_DASH.sub('-',text)))


    def tag_list(self, strict=True):
        tag_words = []
        for (word, word_type) in self._tokenize():
            tag_word = self._cleaned(word, strict)
            if len(tag_word) > MIN_TAG_LENGTH and len(tag_word)<=MAX_TAG_LENGTH and word_type not in STOP_WORDS:
                tag_words.append(tag_word)
        return tag_words

# why lemma not stremming
#https://www.guru99.com/stemming-lemmatization-python-nltk.html
# from nltk.stem import PorterStemmer
        # e_words=[]
        # ps =PorterStemmer()
        # for w in t.tag_list():
        #     rootWord=ps.stem(w)
        #     #print(rootWord)
        #     e_words.append(rootWord)
        # e_words = list(dict.fromkeys(e_words)) 