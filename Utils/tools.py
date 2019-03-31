import re


def find_word(message, words):
    """Looks for one of several words in a string.
    Has not been tested for String instead of a List.
    :param message: String, the string you want to look in.
    :param words: List of words you want to look for.
    :return: True if word is in the message, false if not
    """

    def finder(word):
        return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search

    for w in words:
        if finder(w)(message):
            return True
    return False
