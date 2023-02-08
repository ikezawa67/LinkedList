"""
doubly linked list module
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator, Iterable, MutableSequence
from typing import TypeVar, Generic
from typing import overload

_T = TypeVar('_T')


@dataclass(frozen=True)
class Node(Generic[_T]):
    '''doubly linked node class'''
    value: _T
    prev: Node | None = field(default=None, repr=False)
    next: Node | None = field(default=None, repr=False)


class DoublyLinked(MutableSequence[Node], Generic[_T]):
    'doubly linked list class'

    @overload
    def __init__(self, iterable: None) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[_T]) -> None: ...

    def __init__(self, iterable: Iterable[_T] | None = None) -> None:
        self._first_node: Node[_T] | None = None
        self._last_node: Node[_T] | None = None
        if iterable is not None:
            for _v in iterable:
                self.append(_v)

    def __repr__(self) -> str:
        return [_v for _v in self].__repr__()

    def __len__(self) -> int:
        _len = 0
        node = self._first_node
        while isinstance(node, Node):
            _len += 1
            node = node.next
        return _len

    def _valid_index(self, index: int, _raise: bool = True) -> int:
        _n = len(self)
        if 0 <= index:
            if index > _n:
                if _raise:
                    raise IndexError('list assignment index out of range')
                index = _n
        else:
            if abs(index) > _n + 1:
                if _raise:
                    raise IndexError('list assignment index out of range')
                index = - (_n + 1)
        return index

    @overload
    def __getitem__(self, _i: int) -> Node[_T]: ...
    @overload
    def __getitem__(self, _s: slice) -> DoublyLinked[Node[_T]]: ...

    def __getitem__(self, index: int | slice) -> Node[_T] | DoublyLinked[Node[_T]]:
        if isinstance(index, int):
            if 0 <= index:
                node = self._first_node
                for _ in range(self._valid_index(index)):
                    node = node.next
            else:
                node = self._last_node
                for _ in range(self._valid_index(index), -1):
                    node = node.prev
            if node is None:
                raise IndexError('list assignment index out of range')
            return node
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = DoublyLinked()
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
            if 0 <= index:
                node = self._first_node
                for _ in range(self._valid_index(index)):
                    node = node.next
            else:
                node = self._last_node
                for _ in range(self._valid_index(index), 0):
                    node = node.prev
            if node is None:
                raise IndexError('list assignment index out of range')
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
            if 0 <= index:
                node = self._first_node
                for _ in range(self._valid_index(index)):
                    node = node.next
            else:
                node = self._last_node
                for _ in range(self._valid_index(index), -1):
                    node = node.prev
            if node is self._first_node or node is self._last_node:
                if node is self._first_node:
                    self._first_node = node.next
                    object.__setattr__(node.next, 'prev', None)
                if node is self._last_node:
                    self._last_node = node.prev
                    object.__setattr__(node.prev, 'next', None)
            else:
                object.__setattr__(node.prev, 'next', node.next)
                object.__setattr__(node.next, 'prev', node.prev)
        elif isinstance(index, slice):
            start, stop, stride = index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    def __reversed__(self) -> Iterator[Node[_T]]:
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
    def insert(self, _n: Node[_T], value: _T) -> None: ...

    def insert(self, index: int | Node[_T], value: _T) -> None:
        'S.insert(index, value) -- insert value before index or node'
        if isinstance(index, int):
            node: Node | None = None
            if 0 <= index:
                for i in range(self._valid_index(index, False)):
                    if i == 0:
                        node = self._first_node
                    else:
                        node = node.next
                if node is None:
                    new_node = Node(value, next=self._first_node)
                else:
                    new_node = Node(value, node, node.next)
            else:
                for i in range(0, self._valid_index(index, False), -1):
                    if i == 0:
                        node = self._last_node
                    else:
                        node = node.prev
                if node is None:
                    new_node = Node(value, next=self._first_node)
                else:
                    new_node = Node(value, node, node.next)
            if new_node.prev is None:
                self._first_node = new_node
            else:
                object.__setattr__(new_node.prev, 'next', new_node)
            if new_node.next is None:
                self._last_node = new_node
            else:
                object.__setattr__(new_node.next, 'prev', new_node)
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
        if self._first_node is None or self._last_node is None:
            self._first_node = Node(value)
            self._last_node = self._first_node
        else:
            new_node = Node(value, self._last_node)
            object.__setattr__(self._last_node, 'next', new_node)
            self._last_node = new_node
