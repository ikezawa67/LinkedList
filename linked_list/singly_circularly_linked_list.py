"""
singly circularly linked list module
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, MutableSequence
from typing import TypeVar, Generic
from typing import overload

_T = TypeVar('_T')


@dataclass(init=False, frozen=True)
class Node(Generic[_T]):
    '''singly linked node class'''
    value: _T
    next: Node[_T] = field(repr=False)

    def __init__(self, _value, _next:Node|None = None) -> None:
        object.__setattr__(self, 'value', _value)
        if _next is None:
            object.__setattr__(self, 'next', self)
        else:
            object.__setattr__(self, 'next', _next)


class SinglyCircularlyLinkedList(MutableSequence[Node[_T]], Generic[_T]):
    'singly circularly linked list class'

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
        return [_v for _v in self].__repr__()

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

    def _valid_index(self, index: int) -> int:
        _n = len(self)
        if index < 0:
            index += _n
            if index < 0:
                index = 0
        if index > _n:
            raise IndexError('list assignment index out of range')
        return index

    @overload
    def __getitem__(self, _i: int) -> Node[_T]: ...

    @overload
    def __getitem__(self, _s: slice) -> SinglyCircularlyLinkedList[Node[_T]]: ...

    def __getitem__(self, index: int | slice) -> Node[_T] | SinglyCircularlyLinkedList[Node[_T]]:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            else:
                node = self._last_node.next
                for _ in range(self._valid_index(index)):
                    node = node.next
                return node
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
    def __setitem__(self, _i: int, _v: _T) -> None: ...
    @overload
    def __setitem__(self, _s: slice, _o: Iterable[_T]) -> None: ...

    def __setitem__(self, index: int | slice, value: _T | Iterable[_T]) -> None:
        if isinstance(index, int):
            if self._last_node is None:
                raise IndexError('list assignment index out of range')
            else:
                node = self._last_node.next
                for _ in range(self._valid_index(index)):
                    node = node.next
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
                prev_node = self._last_node
                node = prev_node.next
                for _ in range(self._valid_index(index)):
                    prev_node = node
                    node = node.next
                if node is node.next:
                    self._last_node = None
                else:
                    if node is self._last_node:
                        self._last_node = prev_node
                    object.__setattr__(prev_node, 'next', node.next)
                    object.__setattr__(node.next, 'prev', prev_node)
        elif isinstance(index, slice):
            start, stop, stride = index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(
                f'list indices must be integers or slices, not {type(index)}')

    def insert(self, index: int, value: _T) -> None:
        'S.insert(index, value) -- insert value before index'
        if self._last_node is None:
            self._last_node = Node(value)
        else:
            node = self._last_node.next
            for _ in range(self._valid_index(index) - 1):
                node = node.next
            new_node = Node(value, node.next)
            if node is self._last_node:
                self._last_node = new_node
            object.__setattr__(node, 'next', new_node)

    def append(self, value: _T) -> None:
        'S.append(value) -- append value to the end of the sequence'
        if self._last_node is None:
            self._last_node = Node(value)
        else:
            new_node = Node(value, self._last_node.next)
            object.__setattr__(self._last_node, 'next', new_node)
            self._last_node = new_node
