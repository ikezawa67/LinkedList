"""
singly linked list module
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, MutableSequence
from typing import TypeVar, Generic
from typing import overload

_T = TypeVar('_T')


@dataclass(frozen=True)
class Node(Generic[_T]):
    '''singly linked node class'''
    value: _T
    next: Node[_T] | None = field(default=None, repr=False)


class SinglyLinked(MutableSequence[Node[_T]], Generic[_T]):
    'singly linked list class'

    @overload
    def __init__(self, iterable: None) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[_T]) -> None: ...

    def __init__(self, iterable: Iterable[_T] | None = None) -> None:
        self._first_node: Node[_T] | None = None
        if isinstance(iterable, Iterable):
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
        if index < 0:
            index += _n
            if index < 0:
                index = 0
        if index > _n:
            if _raise:
                raise IndexError('list assignment index out of range')
            index = _n
        return index

    @overload
    def __getitem__(self, _i: int) -> Node[_T]: ...
    @overload
    def __getitem__(self, _s: slice) -> SinglyLinked[Node[_T]]: ...

    def __getitem__(self, index: int | slice) -> Node[_T] | SinglyLinked[Node[_T]]:
        if isinstance(index, int):
            node = self._first_node
            for _ in range(self._valid_index(index)):
                node = node.next
            if node is None:
                raise IndexError('list assignment index out of range')
            return node
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = SinglyLinked()
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
            node = self._first_node
            for _ in range(self._valid_index(index)):
                node = node.next
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
            node = self._first_node
            for _ in range(self._valid_index(index) - 1):
                node = node.next
            if node is None:
                raise IndexError('list assignment index out of range')
            elif node is self._first_node:
                self._first_node = node.next
            else:
                object.__setattr__(node, 'next', node.next.next)
        elif isinstance(index, slice):
            start, stop, stride = index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    @overload
    def insert(self, _i: int, value: _T) -> None: ...
    @overload
    def insert(self, _n: Node[_T], value: _T) -> None: ...

    def insert(self, index: int | Node[_T], value: _T) -> None:
        'S.insert(index, value) -- insert value before index or node'
        if isinstance(index, int):
            node = self._first_node
            for _ in range(self._valid_index(index, False) - 1):
                node = node.next
            if node is None:
                self._first_node = Node(value)
            elif node is self._first_node:
                self._first_node = Node(value, self._first_node)
            else:
                object.__setattr__(node, 'next', Node(value, node.next))
        elif isinstance(index, Node):
            object.__setattr__(index, 'next', Node(value, index.next))
        else:
            raise IndexError('index is an index or a node')
