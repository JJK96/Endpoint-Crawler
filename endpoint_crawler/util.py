class Url(str):
    def __truediv__(self, other):
        return self.rstrip('/') + '/' + other.lstrip('/')
