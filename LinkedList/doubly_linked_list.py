"""
doubly linked list module
"""

from __future__ import annotations
from typing import Iterator, Reversible, Iterable, Collection
from typing import TypeVar, Generic
from typing import Optional, Any, overload

_T = TypeVar('_T')


class DoublyLinkedList(Collection[_T], Reversible[_T], Generic[_T]):
    'singly linked list class'

    class _Node(Generic[_T]):

        def __init__(self, value: _T) -> None:
            self._value = value
            self._prev: Optional[DoublyLinkedList._Node] = None
            self._next: Optional[DoublyLinkedList._Node] = None

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
        def prev(self) -> Optional[DoublyLinkedList._Node]:
            'prev node'
            return self._prev

        @prev.setter
        def prev(self, _prev: Optional[DoublyLinkedList._Node]) -> None:
            if _prev is None:
                self._prev = _prev
            elif isinstance(_prev, type(self)):
                self._prev = _prev
                if _prev.next is not self:
                    _prev.next = self
            else:
                raise TypeError('node next must be _Node or None')

        @property
        def next(self) -> Optional[DoublyLinkedList._Node]:
            'next node'
            return self._next

        @next.setter
        def next(self, _next: Optional[DoublyLinkedList._Node]) -> None:
            if _next is None:
                self._next = None
            elif isinstance(_next, type(self)):
                self._next = _next
                if _next.prev is not self:
                    _next.prev = self
            else:
                raise TypeError('node next must be node')

    def __init__(self, iterable: Optional[Iterable[_T]] = None):
        self._first_node: Optional[DoublyLinkedList._Node] = None
        self._last_node: Optional[DoublyLinkedList._Node] = None
        if iterable is not None:
            for _v in iterable:
                self.append(_v)

    def __repr__(self) -> str:
        return [v for v in self].__repr__()

    def __len__(self) -> int:
        _len = 0
        node = self._first_node
        while isinstance(node, DoublyLinkedList._Node):
            _len += 1
            node = node.next
        return _len

    @overload
    def __getitem__(self, _i: int) -> _T:
        ...

    @overload
    def __getitem__(self, _s: slice) -> DoublyLinkedList[_T]:
        ...

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, int):
            if self._first_node is None:
                raise IndexError('list assignment index out of range')
            elif 0 <= index:
                node = self._first_node
                for _ in range(index):
                    node = node.next
                    if node is None:
                        raise IndexError('list assignment index out of range')
                return node.value
            else:
                node = self._last_node
                for _ in range(1, abs(index)):
                    node = node.prev
                    if node is None:
                        raise IndexError('list assignment index out of range')
                return node.value
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = DoublyLinkedList()
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
            if self._first_node is None:
                raise IndexError('list assignment index out of range')
            elif 0 <= index:
                node = self._first_node
                for _ in range(index):
                    node = node.next
                    if node is None:
                        raise IndexError('list assignment index out of range')
                node.value = value
            else:
                node = self._last_node
                for _ in range(1, abs(index)):
                    node = node.prev
                    if node is None:
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
            if self._first_node is None and self._last_node is None:
                raise IndexError('list assignment index out of range')
            elif 0 <= index:
                new_node = self._first_node
                prev_node = new_node.prev
                for _ in range(index):
                    if new_node is None:
                        raise IndexError('list assignment index out of range')
                    prev_node = new_node
                    new_node = new_node.next
                if prev_node is None:
                    self._first_node = new_node.next
                    if self._first_node is not None:
                        self._first_node.prev = None
                elif new_node.next is None:
                    self._last_node = prev_node
                    if self._last_node is not None:
                        self._last_node.next = None
                else:
                    prev_node.next = new_node.next
            else:
                new_node = self._last_node
                next_node = new_node.next
                for _ in range(abs(index)):
                    if new_node is None:
                        raise IndexError('list assignment index out of range')
                    next_node = new_node
                    new_node = new_node.prev
                if next_node is None:
                    self._last_node = new_node.prev
                    if self._last_node is not None:
                        self._last_node.next = None
                elif new_node.prev is None:
                    self._first_node = next_node
                    if self._first_node is not None:
                        self._first_node.prev = None
                else:
                    next_node.prev = new_node.prev
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

    def __reversed__(self) -> Iterator[_T]:
        _i = -1
        try:
            while True:
                _v = self[_i]
                yield _v
                _i -= 1
        except IndexError:
            return

    def __contains__(self, value: Any) -> bool:
        for _v in self:
            if _v is value or _v == value:
                return True
        return False

    def insert(self, index: int, value: _T) -> None:
        'S.insert(index, value) -- insert value before index'
        if self._first_node is None and self._last_node is None:
            self._first_node = self._Node(value)
            self._last_node = self._first_node
        elif 0 <= index:
            new_node = self._first_node
            prev_node = new_node.prev
            for _ in range(index):
                if new_node is None:
                    break
                prev_node = new_node
                new_node = new_node.next
            node = self._Node(value)
            if prev_node is None:
                self._first_node = node
                self._first_node.next = new_node
            elif new_node is None:
                self._last_node = node
                self._last_node.prev = prev_node
            else:
                prev_node.next = node
                node.next = new_node
        else:
            new_node = self._last_node
            next_node = new_node.next
            for _ in range(abs(index)):
                if new_node is None:
                    break
                next_node = new_node
                new_node = new_node.prev
            node = self._Node(value)
            if next_node is None:
                self._last_node = node
                self._last_node.prev = new_node
            elif new_node is None:
                self._first_node = node
                self._first_node.next = next_node
            else:
                next_node.prev = node
                node.prev = new_node

    def index(self,
              value: Any,
              start: int = 0,
              stop: Optional[int] = None) -> int:
        'S.index(value, [start, [stop]]) -> integer -- return first index of value'
        if start is not None and start < 0:
            start = max(len(self) + start, 0)
        if stop is not None and stop < 0:
            stop += len(self)
        _i = start
        while stop is None or _i < stop:
            try:
                _v = self[_i]
                if _v is value or _v == value:
                    return _i
            except IndexError:
                break
            _i += 1
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
