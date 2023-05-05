from typing import Generic, TypeVar, List

T = TypeVar('T')


class Variable(Generic[T]):
    _value: T = None
    _has_value: bool = False

    def __init__(self, domain: List[T], name: str = None):
        self._domain = domain
        self.name = name
        self.neighbors = set({})

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, x: T):
        if x == self._value:
            return
        if x in self._domain and x is not None:
            self._value = x
            # self._domain.remove(x)
            self._has_value = True
        elif x is None:
            # self._domain.append(self.value)
            self._has_value = False
            self._value = x
        else:
            raise Exception("Value is not in the domain")

    @property
    def domain(self) -> List[T]:
        return self._domain

    @property
    def has_value(self) -> bool:
        return self._has_value

    @domain.setter
    def domain(self, value: List[T]):
        self._domain = value
