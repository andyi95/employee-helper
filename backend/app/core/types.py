class URL(str):
    def __new__(cls, *value):
        if value:
            v0 = value[0]
            if not type(v0) is str:
                raise TypeError('Unexpected type for URL: "%s"' % type(v0))
            if not (v0.startswith('http://') or v0.startswith('https://')):
                raise ValueError('Passed string value "%s" is not an'
                                 ' "http*://" URL' % (v0,))
        # else allow None to be passed. This allows an "empty" URL instance, e.g. `URL()`
        # `URL()` evaluates False

        return str.__new__(cls, *value)
