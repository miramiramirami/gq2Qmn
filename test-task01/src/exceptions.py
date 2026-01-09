class ShortenerBaseException(Exception):
    pass 


class NoLongUrlFoundError(ShortenerBaseException):
    pass
