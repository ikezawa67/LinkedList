"""
singly linked list module
"""

from __future__ import annotations
from typing import TypeVar, Generic, Optional, Iterable, Collection, Any, overload


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

    def __init__(self, iterable: Optional[Iterable[_T]] = None):
        self._first_node: Optional[SinglyLinkedList._Node] = None
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

    def __setitem__(self, index, value):
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

    def __delitem__(self, index: Any):
        if isinstance(index, int):
            if self._first_node is None:
                raise IndexError('list assignment index out of range')
            else:
                if index == 0:
                    delete_node = self._first_node
                    self._first_node = delete_node.next
                    del delete_node
                else:
                    prev_node = self._first_node
                    delete_node = prev_node.next
                    for _ in range(1, index):
                        prev_node = delete_node
                        delete_node = prev_node.next
                        if not isinstance(delete_node, SinglyLinkedList._Node):
                            raise IndexError(
                                'list assignment index out of range')
                    prev_node.next = delete_node.next
                    del delete_node
        elif isinstance(index, slice):
            start, stop, stride = index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    def __iter__(self):
        _i = 0
        try:
            while True:
                _v = self[_i]
                yield _v
                _i += 1
        except IndexError:
            return

    def __contains__(self, value: Any):
        for _v in self:
            if _v is value or _v == value:
                return True
        return False

    def insert(self, index: int, value: _T) -> None:
        'S.insert(index, value) -- insert value before index'
        if self._first_node is None:
            self._first_node = self._Node(value)
        elif index == 0:
            next_node = self._first_node
            self._first_node = self._Node(value)
            self._first_node.next = next_node
        else:
            index = min(index, len(self))
            prev_node = self._first_node
            for _ in range(index - 1):
                prev_node = prev_node.next
            node = self._Node(value)
            node.next = prev_node.next
            prev_node.next = node

    def index(self, value: Any, start: int = 0, stop: Optional[int] = None):
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

    def remove(self, value: _T):
        'S.remove(value) -- remove first occurrence of value'
        del self[self.index(value)]

    def clear(self):
        'S.clear() -> None -- remove all items from S'
        for _v in self:
            self.remove(_v)


a = SinglyLinkedList([1, 2, 3, 4, 5])
print(a)
