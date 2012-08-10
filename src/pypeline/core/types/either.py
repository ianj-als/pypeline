class Either(object):
    def __hash__(self):
        return self.val.__hash__()


class Left(Either):
    def __init__(self, a):
        super(Left, self).__init__()
        self.val = a

    def __eq__(self, other):
        if not isinstance(other, Left):
            return False
        if id(self) == id(other):
            return True
        if self.val == other.val:
            return True

        return False

    def __repr__(self):
        return "<Left: %s>" % self.val


class Right(Either):
    def __init__(self, b):
        super(Right, self).__init__()
        self.val = b

    def __eq__(self, other):
        if not isinstance(other, Right):
            return False
        if id(self) == id(other):
            return True
        if self.val == other.val:
            return True

        return False

    def __repr__(self):
        return "<Right: %s>" % self.val
