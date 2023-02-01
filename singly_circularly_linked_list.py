"""
singly circularly linked list module
"""

from __future__ import annotations
from typing import Iterator, Iterable, Collection
from typing import TypeVar, Generic
from typing import Optional, Any, overload

_T = TypeVar('_T')


class SinglyCircularlyLinkedList(Collection[_T], Generic[_T]):
    'singly circularly linked list class'

    class _Node(Generic[_T]):

        def __init__(self, value: _T) -> None:
            self._value = value
            self._next: SinglyCircularlyLinkedList._Node = self

        @property
        def value(self) -> _T:
            'node value'
            return self._value

        @value.setter
        def value(self, _value: _T) -> None:
            if isinstance(_value, type(self._value)):
                self._value = _value
            else:
                raise TypeError(f'node values must be {type(self._value)}')

        @property
        def next(self) -> SinglyCircularlyLinkedList._Node:
            'next node'
            return self._next

        @next.setter
        def next(self, _next: SinglyCircularlyLinkedList._Node) -> None:
            if isinstance(_next, type(self)):
                self._next = _next
            else:
                raise TypeError('node next must be _Node or None')

    def __init__(self, iterable: Optional[Iterable[_T]] = None) -> None:
        self._last_node: Optional[SinglyCircularlyLinkedList._Node] = None
        if iterable is not None:
            for _v in iterable:
                self.append(_v)

    def __repr__(self) -> str:
        return [v for v in self].__repr__()

    def __len__(self) -> int:
        if self._last_node is None:
            return 0
        else:
            _len = 1
            node = self._last_node.next
            while node is not self._last_node:
                _len += 1
                node = node.next
            return _len

    @overload
    def __getitem__(self, _i: int) -> _T:
        ...

    @overload
    def __getitem__(self, _s: slice) -> SinglyCircularlyLinkedList[_T]:
        ...

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            else:
                node = self._last_node.next
                for _ in range(index):
                    node = node.next
                    if node is self._last_node.next:
                        raise IndexError('list assignment index out of range')
                return node.value
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = SinglyCircularlyLinkedList()
            for _i in range(start, stop, step):
                result.append(self[_i])
            return result
        else:
            raise IndexError(
                f'list indices must be integers or slices, not {type(index)}')

    @overload
    def __setitem__(self, _i: int, _v: _T) -> None:
        ...

    @overload
    def __setitem__(self, _s: slice, _o: Iterable[_T]) -> None:
        ...

    def __setitem__(self, index: Any, value: Any) -> None:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            else:
                node = self._last_node.next
                for _ in range(index):
                    node = node.next
                    if node is self._last_node.next:
                        raise IndexError('list assignment index out of range')
                node.value = value
        elif isinstance(index, slice):
            if isinstance(value, Iterable):
                start, stop, stride = index.indices(len(self))
                for _i, _v in zip(range(start, stop, stride), value):
                    self[_i] = _v
            else:
                raise TypeError('can only assign an iterable')
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    @overload
    def __delitem__(self, _i: int) -> None:
        ...

    @overload
    def __delitem__(self, _s: slice) -> None:
        ...

    def __delitem__(self, index: Any) -> None:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            else:
                prev_node = self._last_node
                new_node = self._last_node.next
                for _ in range(index):
                    if new_node is self._last_node.next:
                        raise IndexError('list assignment index out of range')
                    prev_node = new_node
                    new_node = new_node.next
                if new_node is self._last_node:
                    prev_node.next = new_node.next
                    if prev_node.next is prev_node:
                        self._last_node = None
                    else:
                        self._last_node = prev_node
                else:
                    prev_node.next = new_node.next
                del new_node
        elif isinstance(index, slice):
            start, stop, stride = index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    def __iter__(self) -> Iterator[_T]:
        _i = 0
        try:
            while True:
                _v = self[_i]
                yield _v
                _i += 1
        except IndexError:
            return

    def __contains__(self, value: Any) -> bool:
        for _v in self:
            if _v is value or _v == value:
                return True
        return False

    def insert(self, index: int, value: _T, circulate: bool = False) -> None:
        'S.insert(index, value) -- insert value before index'
        if self._last_node is None:
            self._last_node = self._Node(value)
        else:
            prev_node = self._last_node
            new_node = self._last_node.next
            for _ in range(index):
                if circulate and new_node is self._last_node.next:
                    break
                prev_node = new_node
                new_node = new_node.next
            node = self._Node(value)
            if prev_node is self._last_node:
                prev_node.next = node
                self._last_node = node
                self._last_node.next = new_node
            else:
                prev_node.next = node
                node.next = new_node

    def index(self,
              value: Any,
              start: Optional[int] = None,
              stop: Optional[int] = None) -> int:
        'S.index(value, [start, [stop]]) -> integer -- return first index of value'
        start = max(0, start) if isinstance(start, int) else 0
        stop = min(stop, len(self)) if isinstance(stop, int) else len(self)
        for _i in range(start, stop):
            _v = self[_i]
            if _v is value or _v == value:
                return _i
        raise ValueError()

    def append(self, value: _T) -> None:
        'S.append(value) -- append value to the end of the sequence'
        self.insert(len(self), value)

    def remove(self, value: _T) -> None:
        'S.remove(value) -- remove first occurrence of value'
        del self[self.index(value)]

    def clear(self) -> None:
        'S.clear() -> None -- remove all items from S'
        for _ in range(len(self)):
            del self[0]


a = SinglyCircularlyLinkedList([1, 2, 3, 4, 5])
print(a)
a.clear()
print(a)
a.insert(1000, 10, True)
a.insert(1000, 11, True)
a.insert(1000, 12, True)
print(a)
