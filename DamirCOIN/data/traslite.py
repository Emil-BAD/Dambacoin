import translators as ts


def traslite(text):
    return ts.bing(text, to_language='ru')
