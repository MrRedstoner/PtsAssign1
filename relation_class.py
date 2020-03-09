import operator
from collections import defaultdict
from functools import reduce


def get_relation_class(a: set) -> type:
    objects = frozenset(a)

    class RelClass:
        def __init__(self):
            self._objects = objects
            self._relation = defaultdict(set)

        def _check_element(self, elem) -> None:
            assert type(elem) is tuple, "Please make sure the element is a tuple"
            assert len(elem) == 2, "Please make sure element is a 2-tuple"
            assert elem[0] in self._objects, "{0} must be in {1}".format(elem[0], self._objects)
            assert elem[1] in self._objects, "{0} must be in {1}".format(elem[1], self._objects)

        def _check_relation(self, other) -> None:
            assert type(self) == type(other), "Please use the same type for both objects"

        def __contains__(self, item: tuple) -> bool:
            self._check_element(item)
            return item[1] in self._relation[item[0]]

        def __add__(self, other: tuple) -> 'RelClass':
            self._check_element(other)
            out = RelClass()
            out._relation = self._relation.copy()
            out._relation[other[0]] = {*self._relation[other[0]], other[1]}
            return out

        def _sub_element(self, other: tuple) -> 'RelClass':
            if other not in self:
                return self
            self._check_element(other)
            out = RelClass()
            out._relation = self._relation.copy()
            out._relation[other[0]] = out._relation[other[0]].copy()
            out._relation[other[0]].remove(other[1])
            return out

        def _sub_rel_class(self, other: 'RelClass') -> 'RelClass':
            self._check_relation(other)
            out = RelClass()
            for first, seconds in self._relation.items():
                out._relation[first] = seconds.copy()
            for first in self._objects:
                out._relation[first] -= other._relation[first]
            return out

        def __sub__(self, other) -> 'RelClass':
            if type(other) == tuple:
                return self._sub_element(other)
            else:
                return self._sub_rel_class(other)

        def __or__(self, other: 'RelClass') -> 'RelClass':
            self._check_relation(other)
            out = RelClass()
            for first, seconds in self._relation.items():
                out._relation[first] = seconds.copy()
            for first, seconds in other._relation.items():
                out._relation[first] |= seconds;
            return out

        union = __or__

        def __and__(self, other: 'RelClass') -> 'RelClass':
            self._check_relation(other)
            out = RelClass()
            for first, seconds in self._relation.items():
                out._relation[first] = seconds.copy()
            for first in self._objects:
                out._relation[first] &= other._relation[first]
            return out

        intersection = __and__

        def __invert__(self) -> 'RelClass':
            out = RelClass()
            for first, seconds in self._relation.items():
                for second in seconds:
                    out._relation[second].add(first)
            return out

        invert = __invert__

        def __pow__(self, other: 'RelClass') -> 'RelClass':
            self._check_relation(other)
            out = RelClass()
            for first, seconds in self._relation.items():
                out._relation[first] = reduce(operator.or_, map(other._relation.get, seconds))
            return out

        compose = __pow__

        def __str__(self) -> str:
            return "{" + ', '.join(str(first) + ':' +
                                   ("{" + ', '.join(str(second) for second in seconds) + "}")
                                   for first, seconds in self._relation.items()) + "}"

    return RelClass
