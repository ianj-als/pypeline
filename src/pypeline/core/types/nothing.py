from pypeline.core.types.monad import Maybe


#
# Nothing. This is a singleton.
#
class Nothing(Maybe):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Nothing, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __ge__(self, function):
        return Nothing()

    def __repr__(self):
        return "<Nothing>"

    def __nonzero__(self):
        return False


def return_(a):
    return Nothing()
