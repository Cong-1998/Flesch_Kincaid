import re


def count(word):
    """
    Simple syllable counting
    """

    word = word if type(word) is str else str(word)

    word = word.lower()

    if len(word) <= 3:
        return 1

    count = 0

    if word.endswith('ly'):
        count = 1
        word = word[:-2]
        
    if word.endswith('ment') or word.endswith('ness'):
        count = 1
        word = word[:-4]

    if word.endswith('ed'):
        count = 0
        word = word[:-2]

    word = re.sub('(?:[^laeiouy]es|[^laeiouy]e)$', '', word) # removed ed|
    word = re.sub('^y', '', word)
    matches = re.findall('[aeiouy]{1,2}', word)
    
    return len(matches)+count
