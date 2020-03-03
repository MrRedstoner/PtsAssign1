def add_to_set(s: set, elem) -> set:
    out = s.copy()
    out.add(elem)
    return out


def get_relation_class(a: set) -> type:
    class RelClass:
        def __init__(self):
            self._objects = frozenset(a)
            self._relation = dict()

        def _check_element(self, elem):
            assert type(elem) is tuple, "Please make sure the element is a tuple"
            assert len(elem) == 2, "Please make sure element is a 2-tuple"
            assert elem[0] in self._objects, "{0} must be in {1}".format(elem[0], self._objects)
            assert elem[1] in self._objects, "{0} must be in {1}".format(elem[1], self._objects)

        def __contains__(self, item: tuple):
            self._check_element(item)
            return item[1] in self._relation.get(item[0], set())

        def __add__(self, other: tuple):
            self._check_element(other)
            out = RelClass()
            out._objects = self._objects
            out._relation = self._relation.copy()
            out._relation[other[0]] = add_to_set(self._relation.get(other[0], set()), other[1])
            return out

        def __str__(self) -> str:
            return str(self._relation)

    return RelClass
