'''singly circularly linked list module'''
from __future__ import annotations
import sys
from typing import Any
from typing import TypeVar, Generic, Type, Self, Iterable, MutableSequence
from typing import overload

_T = TypeVar('_T')


class Node(Generic[_T]):
    '''singly circularly node class'''
    def __new__(cls: Type[Self[_T]], _value: _T, _next: Node | None = None) -> Node:
        try:
            if 'next' in vars(_value):
                raise Exception('_Node \'value\' must not have \'next\'')
        except TypeError:
            pass
        try:
            _cls = type('_Node', (type(_value), ), {'next': _next})
        except TypeError:
            _cls = type('_Node', (object, ), {'next': _next})
        _cls.__init__ = Node.__init__
        _cls.__setattr__ = Node.__setattr__
        _cls.__slots__ = ('next', )
        return _cls(_value)

    def __init__(self: Self, _value: _T, _next: Node | None = None) -> None:
        self.next: Node

    def __setattr__(self: Self, _name: str, _value: Any) -> None:
        try:
            if _name == 'next':
                raise Exception('cannot assign to field \'next\'')
        except AttributeError:
            pass
        object.__setattr__(_name, _value)


class List(MutableSequence[Node[_T]], Generic[_T]):
    'singly circularly linked list class'
    __slots__ = ('_head', '_tail', )

    @overload
    def __init__(self: Self) -> None: ...
    @overload
    def __init__(self: Self, __i: Iterable[_T]) -> None: ...

    def __init__(self: Self, _iterable: Iterable[_T] | None = None) -> None:
        self._head: Node[None] = Node(None)
        self._tail: Node[None] | Node[_T] = self._head
        object.__setattr__(self._tail, 'next', self._head)
        if isinstance(_iterable, Iterable):
            for _v in _iterable:
                self.append(_v)

    def __repr__(self: Self) -> str:
        return repr([_v for _v in self])

    def __sizeof__(self: Self) -> int:
        return sys.getsizeof(self._head) + sum([sys.getsizeof(_v) for _v in self])

    def __len__(self: Self) -> int:
        _len = 0
        node = self._head.next
        while True:
            if node is self._head:
                break
            node = node.next
            _len += 1
        return _len

    def _valid_index(self: Self, _index: int, _raise: bool = True) -> int:
        _n = len(self)
        if _index < 0:
            _index += _n
            if _index < 0:
                _index = 0
        if _index > _n:
            if _raise:
                raise IndexError('list assignment index out of range')
            _index = _n
        return _index

    @overload
    def __getitem__(self: Self, __i: int) -> Node[_T]: ...
    @overload
    def __getitem__(self: Self, __s: slice) -> Self[Node[_T]]: ...

    def __getitem__(self: Self, _index: int | slice) -> Node[_T] | Self[Node[_T]]:
        if isinstance(_index, int):
            node = self._head.next
            if node is self._head:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                node = node.next
                if node is self._head:
                    raise IndexError('list assignment index out of range')
            return node
        elif isinstance(_index, slice):
            start, stop, step = _index.indices(len(self))
            return List([self[_i] for _i in range(start, stop, step)])
        else:
            raise IndexError(f'list indices must be integers or slices, not {type(_index)}')

    @overload
    def __setitem__(self: Self, __i: int, __v: _T) -> None: ...
    @overload
    def __setitem__(self: Self, __s: slice, __o: Iterable[_T]) -> None: ...

    def __setitem__(self: Self, _index: int | slice, _value: _T | Iterable[_T]) -> None:
        if isinstance(_index, int):
            prev = self._head
            node = prev.next
            if node is self._head:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                prev = node
                node = prev.next
                if node is self._head:
                    raise IndexError('list assignment index out of range')
            object.__setattr__(prev, 'next', Node(_value, node.next))
            del node
        elif isinstance(_index, slice):
            if isinstance(_value, Iterable):
                start, stop, stride = _index.indices(len(self))
                for _i, _v in zip(range(start, stop, stride), _value):
                    self[_i] = _v
            else:
                raise TypeError('can only assign an iterable')
        else:
            raise TypeError(f'list indices must be integers or slices, not {type(_index)}')

    @overload
    def __delitem__(self: Self, __i: int) -> None: ...
    @overload
    def __delitem__(self: Self, __s: slice) -> None: ...

    def __delitem__(self: Self, _index: int | slice) -> None:
        if isinstance(_index, int):
            prev = self._head
            node = prev.next
            if node is self._head:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                prev = node
                node = prev.next
                if node is self._head:
                    raise IndexError('list assignment index out of range')
            object.__setattr__(prev, 'next', node.next)
            if prev.next is self._head:
                self._tail = self._head
            del node
        elif isinstance(_index, slice):
            start, stop, stride = _index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(f'list indices must be integers or slices, not {type(_index)}')

    @overload
    def insert(self: Self, __i: int, __v: _T) -> None: ...
    @overload
    def insert(self: Self, __n: Node[_T], __v: _T) -> None: ...

    def insert(self: Self, _index: int | Node[_T], _value: _T) -> None:
        'S.insert(index, value) -- insert value before index'
        try:
            node = Node(_value, _index.next)
            object.__setattr__(_index, 'next', node)
            if node.next is self._head:
                self._tail = node
        except AttributeError as exc:
            if isinstance(_index, int):
                _index = self._valid_index(_index, False)
                if _index == 0:
                    object.__setattr__(self._head, 'next', Node(_value, self._head.next))
                else:
                    self.insert(self[_index - 1], _value)
            else:
                raise IndexError('index is an index or a node') from exc

    def append(self, _value: _T) -> None:
        'S.append(value) -- append value to the end of the sequence'
        node = Node(_value, self._head)
        object.__setattr__(self._tail, 'next', node)
        self._tail = node

    def reverse(self: Self):
        'S.reverse() -- reverse *IN PLACE*'
        _n = len(self)
        for i in range(_n // 2):
            prev_0, prev_1 = self._head if i == 0 else self[i - 1], self[_n - i - 2]
            node_0, node_1 = prev_0.next, prev_1.next
            next_0, next_1 = node_0.next, node_1.next
            object.__setattr__(prev_0, 'next', node_1)
            object.__setattr__(prev_1, 'next', node_0)
            object.__setattr__(node_0, 'next', next_1)
            if next_0 is node_1:
                object.__setattr__(node_1, 'next', node_0)
            else:
                object.__setattr__(node_1, 'next', next_0)
            if node_1 is self._tail:
                self._tail = node_0
