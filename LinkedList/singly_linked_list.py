"""
singly linked list module
"""

from __future__ import annotations
from typing import Iterator, TypeVar, Generic, Optional, Iterable, Collection, Any, overload


_T = TypeVar('_T')


class SinglyLinkedList(Collection[_T], Generic[_T]):
    'singly linked list class'
    class _Node(Generic[_T]):
        def __init__(self, value: _T) -> None:
            self._value = value
            self._next: Optional[SinglyLinkedList._Node] = None

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
        def next(self) -> Optional[SinglyLinkedList._Node]:
            'next node'
            return self._next

        @next.setter
        def next(self, _next: Optional[SinglyLinkedList._Node]) -> None:
            if isinstance(_next, type(self)) or _next is None:
                self._next = _next
            else:
                raise TypeError('node next must be node')

    def __init__(self, iterable: Optional[Iterable[_T]] = None) -> None:
        self._first_node: Optional[SinglyLinkedList._Node] = None
        if iterable is not None:
            for _v in iterable:
                self.append(_v)

    def __repr__(self) -> str:
        return [v for v in self].__repr__()

    def __len__(self) -> int:
        _len = 0
        node = self._first_node
        while isinstance(node, SinglyLinkedList._Node):
            _len += 1
            node = node.next
        return _len

    @overload
    def __getitem__(self, _i: int) -> _T: ...
    @overload
    def __getitem__(self, _s: slice) -> SinglyLinkedList[_T]: ...

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, int):
            if self._first_node is None:
                raise IndexError('list assignment index out of range')
            else:
                node = self._first_node
                for _ in range(index):
                    node = node.next
                    if node is None:
                        raise IndexError('list assignment index out of range')
                return node.value
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = SinglyLinkedList()
            for _i in range(start, stop, step):
                result.append(self[_i])
            return result
        else:
            raise IndexError(
                f'list indices must be integers or slices, not {type(index)}')

    @overload
    def __setitem__(self, _i: int, _v: _T) -> None: ...
    @overload
    def __setitem__(self, _s: slice, _o: Iterable[_T]) -> None: ...

    def __setitem__(self, index, value) -> None:
        if isinstance(index, int):
            if self._first_node is None:
                raise IndexError('list assignment index out of range')
            else:
                node = self._first_node
                for _ in range(index):
                    node = node.next
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
    def __delitem__(self, _i: int) -> None: ...
    @overload
    def __delitem__(self, _s: slice) -> None: ...

    def __delitem__(self, index: Any) -> None:
        if isinstance(index, int):
            if self._first_node is None:
                raise IndexError('list assignment index out of range')
            else:
                prev_node = None
                new_node = self._first_node
                for _ in range(index):
                    if new_node is None:
                        raise IndexError('list assignment index out of range')
                    prev_node = new_node
                    new_node = new_node.next
                if prev_node is None:
                    self._first_node = new_node.next
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

    def insert(self, index: int, value: _T) -> None:
        'S.insert(index, value) -- insert value before index'
        if 0 == len(self):
            self._first_node = self._Node(value)
        else:
            prev_node = None
            new_node = self._first_node
            for _ in range(index):
                if new_node is None:
                    break
                prev_node = new_node
                new_node = new_node.next
            node = self._Node(value)
            if prev_node is None:
                self._first_node = node
                self._first_node.next = new_node
            else:
                prev_node.next = node
                node.next = new_node

    def index(self, value: Any, start: Optional[int] = None, stop: Optional[int] = None) -> int:
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
