#
# Base monad class
#
class Monad(object):
    # return
    # return :: a -> m a
    def return_(self, a):
        raise NotImplementedError

    # Bind operator
    # (>>=) :: m a -> (a -> m b) -> m b
    def __ge__(self, other):
        raise NotImplementedError

    # Bind "Shove" operator
    # (>>) :: m a -> m b -> m b
    def __rshift__(self, other):
        if not isinstance(other):
            raise ValueError("Must be a monadic type")
        return self >= (lambda _: other)


#
# Erm, maybe...
#
class Maybe(Monad):
    pass

