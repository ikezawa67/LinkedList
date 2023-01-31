from __future__ import annotations
from typing import TypeVar, Generic, Optional, Iterable, Iterator, Collection, Any, overload

_T = TypeVar('_T')


class SinglyLinkedNode(Generic[_T]):

    def __init__(self, value: _T) -> None:
        self._value = value
        self._next: Optional[SinglyLinkedNode] = None

    @property
    def value(self) -> _T:
        return self._value

    @value.setter
    def value(self, _value: _T) -> None:
        if isinstance(_value, type(self._value)):
            self._value = _value
        else:
            raise TypeError()

    @property
    def next(self) -> Optional[SinglyLinkedNode]:
        return self._next

    @next.setter
    def next(self, _next: Optional[SinglyLinkedNode]) -> None:
        if isinstance(_next, type(self)) or _next is None:
            self._next = _next
        else:
            raise TypeError()


class SinglyLinkedList(Collection[_T], Generic[_T]):

    def __init__(self, iterable: Optional[Iterable[_T]] = None):
        self._first_node: Optional[SinglyLinkedNode] = None
        for v in iterable:
            self.append(v)

    def __repr__(self) -> str:
        return [v for v in self].__repr__()

    def __len__(self) -> int:
        _len = 0
        node = self._first_node
        while isinstance(node, SinglyLinkedNode):
            _len += 1
            node = node.next
        return _len

    @overload
    def __getitem__(self, i: int) -> _T:
        ...

    @overload
    def __getitem__(self, s: slice) -> SinglyLinkedList[_T]:
        ...

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, int):
            if self._first_node is None:
                raise IndexError()
            else:
                count = 0
                node = self._first_node
                while count < index:
                    if node.next is None:
                        raise IndexError()
                    count += 1
                    node = node.next
                return node.value
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = None
            for i in range(start, stop, step):
                if result is None:
                    result = SinglyLinkedList(self[i])
                else:
                    result.append(self[i])
            return result
        else:
            raise IndexError()

    @overload
    def __setitem__(self, i: int, v: _T) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[_T]) -> None:
        ...

    def __setitem__(self, index, value):
        raise IndexError

    @overload
    def __delitem__(self, i: int) -> None:
        ...

    @overload
    def __delitem__(self, s: slice) -> None:
        ...

    def __delitem__(self, index):
        raise IndexError

    def __iter__(self):
        i = 0
        try:
            while True:
                v = self[i]
                yield v
                i += 1
        except IndexError:
            return

    def __contains__(self, value: Any):
        for v in self:
            if v is value or v == value:
                return True
        return False

    def insert(self, index: int, value: _T) -> None:
        if self._first_node is None:
            self._first_node = SinglyLinkedNode(value)
        elif index == 0:
            next_node = self._first_node
            self._first_node = SinglyLinkedNode(value)
            self._first_node.next = next_node
        else:
            index = min(index, len(self))
            prev_node = self._first_node
            for _ in range(index - 1):
                prev_node = prev_node.next
            node = SinglyLinkedNode(value)
            node.next = prev_node.next
            prev_node.next = node

    def index(self, value: Any, start: int = 0, stop: Optional[int] = None):
        if start is not None and start < 0:
            start = max(len(self) + start, 0)
        if stop is not None and stop < 0:
            stop += len(self)
        i = start
        while stop is None or i < stop:
            try:
                v = self[i]
                if v is value or v == value:
                    return i
            except IndexError:
                break
            i += 1
        raise ValueError()

    def append(self, value: _T) -> None:
        self.insert(len(self), value)

    def remove(self, value: _T):
        del self[self.index(value)]

    def clear(self):
        for v in self:
            self.remove(v)


a = SinglyLinkedList([1, 2, 3, 4, 5])
print(a)
