from collections import defaultdict


def get_relation_class(a: set) -> type:
    class RelClass:
        def __init__(self):
            self._objects = frozenset(a)
            self._relation = defaultdict(set)

        def _check_element(self, elem) -> None:
            assert type(elem) is tuple, "Please make sure the element is a tuple"
            assert len(elem) == 2, "Please make sure element is a 2-tuple"
            assert elem[0] in self._objects, "{0} must be in {1}".format(elem[0], self._objects)
            assert elem[1] in self._objects, "{0} must be in {1}".format(elem[1], self._objects)

        def __contains__(self, item: tuple) -> bool:
            self._check_element(item)
            return item[1] in self._relation[item[0]]

        def __add__(self, other: tuple):
            self._check_element(other)
            out = RelClass()
            out._objects = self._objects
            out._relation = self._relation.copy()
            out._relation[other[0]] = {*self._relation[other[0]], other[1]}
            return out

        def __sub__(self, other: tuple):
            if other not in self:
                return self
            self._check_element(other)
            out = RelClass()
            out._objects = self._objects
            out._relation = self._relation.copy()
            out._relation[other[0]] = out._relation[other[0]].copy()
            out._relation[other[0]].remove(other[1])
            return out

        def __str__(self) -> str:
            return str(self._relation)

    return RelClass
