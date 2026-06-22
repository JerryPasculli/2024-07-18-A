class Arco:
    def __init__(self, p, s, pe):
        self._primo = p
        self._secondo = s
        self._peso = pe

    def __lt__(self, other):
        return self._peso<other._peso