'''singly linked list module'''
from __future__ import annotations
import sys
from typing import Any
from typing import TypeVar, Generic, Type, Self, Iterable, MutableSequence
from typing import overload

_T = TypeVar('_T')


class Node(Generic[_T]):
    'singly linked node class'
    def __new__(cls: Type[Self[_T]], _value: _T, _next: Node | None = None) -> Node:
        try:
            if 'next' in vars(_value):
                raise Exception('node \'value\' must not have \'next\'')
        except TypeError:
            pass
        try:
            _cls = type('Node', (type(_value), ), {'next': _next})
        except TypeError:
            _cls = type('Node', (object, ), {'next': _next})
        _cls.__init__ = Node.__init__
        _cls.__setattr__ = Node.__setattr__
        _cls.__slots__ = ('next', )
        return _cls(_value)

    def __init__(self: Self, _value: _T, _next: Node | None = None) -> None:
        self.next: Node | None

    def __setattr__(self: Self, _name: str, _value: Any) -> None:
        if _name == 'next':
            raise AttributeError('cannot assign to field \'next\'')
        object.__setattr__(_name, _value)


class List(MutableSequence[Node[_T]], Generic[_T]):
    'singly linked list class'
    __slots__ = ('head', 'tail', )

    @overload
    def __init__(self: Self) -> None: ...
    @overload
    def __init__(self: Self, __i: Iterable[_T]) -> None: ...

    def __init__(self: Self, _iterable: Iterable[_T] | None = None) -> None:
        self.head: Node[None]
        self.tail: Node[_T] | Node[None]
        object.__setattr__(self, 'head', Node(None))
        object.__setattr__(self, 'tail', self.head)
        if isinstance(_iterable, Iterable):
            for _v in _iterable:
                self.append(_v)

    def __setattr__(self: Self, _name: str, _value: Any) -> None:
        if _name in self.__slots__:
            raise AttributeError('cannot assign to field \'head\' and \'tail\'')
        object.__setattr__(_name, _value)

    def __repr__(self: Self) -> str:
        return repr([_v for _v in self])

    def __sizeof__(self: Self) -> int:
        return sys.getsizeof(self.head) + sum([sys.getsizeof(_v) for _v in self])

    def __len__(self: Self) -> int:
        _len = 0
        node = self.head.next
        while True:
            try:
                node = node.next
            except AttributeError:
                break
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
            node = self.head.next
            if node is None:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                node = node.next
                if node is None:
                    raise IndexError('list assignment index out of range')
            return node
        elif isinstance(_index, slice):
            start, stop, step = _index.indices(len(self))
            return List([self[_i] for _i in range(start, stop, step)])
        else:
            raise IndexError(f'index must be integers or slices, not {type(_index)}')

    @overload
    def __setitem__(self: Self, __i: int, __v: _T) -> None: ...
    @overload
    def __setitem__(self: Self, __s: slice, __o: Iterable[_T]) -> None: ...

    def __setitem__(self: Self, _index: int | slice, _value: _T | Iterable[_T]) -> None:
        if isinstance(_index, int):
            prev = self.head
            node = prev.next
            if node is None:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                prev = node
                node = prev.next
                if node is None:
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
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    @overload
    def __delitem__(self: Self, __i: int) -> None: ...
    @overload
    def __delitem__(self: Self, __s: slice) -> None: ...

    def __delitem__(self: Self, _index: int | slice) -> None:
        if isinstance(_index, int):
            prev = self.head
            node = prev.next
            if node is None:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                prev = node
                node = prev.next
                if node is None:
                    raise IndexError('list assignment index out of range')
            object.__setattr__(prev, 'next', node.next)
            if prev.next is None:
                object.__setattr__(self, 'tail', prev)
            del node
        elif isinstance(_index, slice):
            start, stop, stride = _index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    @overload
    def insert(self: Self, __i: int, __v: _T) -> None: ...
    @overload
    def insert(self: Self, __n: Node[_T], __v: _T) -> None: ...
    @overload
    def insert(self: Self, __n: Node[None], __v: _T) -> None: ...

    def insert(self: Self, _index: int | Node[_T] | Node[None], _value: _T) -> None:
        'insert value next to index or node'
        try:
            node = Node(_value, _index.next)
            object.__setattr__(_index, 'next', node)
            if node.next is None:
                object.__setattr__(self, 'tail', node)
        except AttributeError as exc:
            if isinstance(_index, int):
                node = self.head
                for _ in range(self._valid_index(_index, False)):
                    if node.next is None:
                        break
                    node = node.next
                self.insert(node, _value)
            else:
                raise IndexError('index must be integers or a node') from exc

    def append(self: Self, _value: _T) -> None:
        'append value to the end of the sequence'
        node = Node(_value)
        object.__setattr__(self.tail, 'next', node)
        object.__setattr__(self, 'tail', node)

    def reverse(self: Self):
        'reverse the list'
        _n = len(self)
        for i in range(_n // 2):
            prev_0, prev_1 = self.head if i == 0 else self[i - 1], self[_n - i - 2]
            node_0, node_1 = prev_0.next, prev_1.next
            next_0, next_1 = node_0.next, node_1.next
            object.__setattr__(prev_0, 'next', node_1)
            object.__setattr__(prev_1, 'next', node_0)
            object.__setattr__(node_0, 'next', next_1)
            if next_0 is node_1:
                object.__setattr__(node_1, 'next', node_0)
            else:
                object.__setattr__(node_1, 'next', next_0)
            if node_1 is self.tail:
                object.__setattr__(self, 'tail', node_0)
