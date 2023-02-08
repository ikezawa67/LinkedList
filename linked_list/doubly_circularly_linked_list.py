"""
doubly circularly linked list module
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator, Iterable, MutableSequence
from typing import TypeVar, Generic
from typing import overload

_T = TypeVar('_T')


@dataclass(init=False, frozen=True)
class Node(Generic[_T]):
    '''doubly linked node class'''
    value: _T
    prev: Node = field(repr=False)
    next: Node = field(repr=False)

    def __init__(self, _value, _prev: Node | None = None, _next: Node | None = None) -> None:
        object.__setattr__(self, 'value', _value)
        if _prev is None:
            object.__setattr__(self, 'prev', self)
        else:
            object.__setattr__(self, 'prev', _prev)
        if _next is None:
            object.__setattr__(self, 'next', self)
        else:
            object.__setattr__(self, 'next', _next)


class DoublyCircularlyLinkedList(MutableSequence[Node[_T]], Generic[_T]):
    'doubly circularly linked list class'

    @overload
    def __init__(self, iterable: None) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[_T]) -> None: ...

    def __init__(self, iterable: Iterable[_T] | None = None) -> None:
        self._last_node: Node[_T] | None = None
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

    def _valid_index(self, index: int, _raise: bool = True) -> int:
        if 0 <= index:
            _n = len(self) - 1
            if index > _n:
                if _raise:
                    raise IndexError('list assignment index out of range')
                index = _n
        else:
            _n = len(self)
            if abs(index) > _n:
                if _raise:
                    raise IndexError('list assignment index out of range')
                index = -_n
        return index

    @overload
    def __getitem__(self, _i: int) -> Node[_T]: ...

    @overload
    def __getitem__(
        self, _s: slice) -> DoublyCircularlyLinkedList[Node[_T]]: ...

    def __getitem__(self, index: int | slice) -> Node[_T] | DoublyCircularlyLinkedList[Node[_T]]:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            elif 0 <= index:
                node = self._last_node.next
                for _ in range(self._valid_index(index)):
                    node = node.next
                return node
            else:
                node = self._last_node
                for _ in range(self._valid_index(index), -1):
                    node = node.prev
                return node
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = DoublyCircularlyLinkedList()
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

    def __setitem__(self, index: int | slice, value: _T | Iterable[_T]) -> None:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            elif 0 <= index:
                node = self._last_node.next
                for _ in range(self._valid_index(index)):
                    node = node.next
                object.__setattr__(node, 'value', value)
            else:
                node = self._last_node
                for _ in range(self._valid_index(index), -1):
                    node = node.prev
                object.__setattr__(node, 'value', value)
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

    def __delitem__(self, index: int | slice) -> None:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            else:
                if 0 <= index:
                    node = self._last_node.next
                    for _ in range(self._valid_index(index)):
                        node = node.next
                else:
                    node = self._last_node
                    for _ in range(self._valid_index(index), -1):
                        node = node.prev
                if node is node.next:
                    self._last_node = None
                else:
                    if node is self._last_node:
                        self._last_node = node.prev
                    object.__setattr__(node.prev, 'next', node.next)
                    object.__setattr__(node.next, 'prev', node.prev)
        elif isinstance(index, slice):
            start, stop, stride = index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    def __reversed__(self) -> Iterator[_T]:
        _i = -1
        try:
            while True:
                _v = self[_i]
                yield _v
                _i -= 1
        except IndexError:
            return

    @overload
    def insert(self, _i: int, value: _T) -> None: ...
    @overload
    def insert(self, _n: Node, value: _T) -> None: ...

    def insert(self, index: int, value: _T | Node[_T]) -> None:
        'S.insert(index, value) -- insert value before index'
        if isinstance(index, int):
            if self._last_node is None:
                self._last_node = Node(value)
            else:
                if 0 <= index:
                    node = self._last_node.next
                    for _ in range(self._valid_index(index)):
                        node = node.next
                else:
                    node = self._last_node
                    for _ in range(self._valid_index(index), -1):
                        node = node.prev
                new_node = Node(value, node, node.next)
                object.__setattr__(node.next, 'prev', new_node)
                object.__setattr__(node, 'next', new_node)
                if node is self._last_node:
                    self._last_node = node.next
        elif isinstance(index, Node):
            node = Node(value, index, index.next)
            object.__setattr__(index, 'next', node)
            object.__setattr__(node, 'prev', index)
            if node.next is None:
                self._last_node = node
        else:
            raise IndexError('index is an index or a node')

    def append(self, value: _T) -> None:
        'S.append(value) -- append value to the end of the sequence'
        if self._last_node is None:
            self._last_node = Node(value)
        else:
            next_node = self._last_node.next
            self._last_node.next = Node(value)
            self._last_node = self._last_node.next
            self._last_node.next = next_node
