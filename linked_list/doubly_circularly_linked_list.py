'''doubly circularly linked list module'''
from __future__ import annotations
import sys
from typing import Any, Iterator
from typing import TypeVar, Generic, Type, Self, Iterable, MutableSequence
from typing import overload

_T = TypeVar('_T')


class Node(Generic[_T]):
    'doubly circularly linked node class'
    def __new__(cls: Type[Self[_T]], _value: _T, _prev: Node | None = None, _next: Node | None = None) -> Node:
        try:
            if 'prev' in vars(_value) or 'next' in vars(_value):
                raise Exception('node \'value\' must not have \'prev\' and \'next\'')
        except TypeError:
            pass
        try:
            _cls = type('Node', (type(_value), ), {'prev': _prev, 'next': _next})
        except TypeError:
            _cls = type('Node', (object, ), {'prev': _prev, 'next': _next})
        _cls.__init__ = Node.__init__
        _cls.__setattr__ = Node.__setattr__
        _cls.__slots__ = ('next', 'prev', )
        return _cls(_value)

    def __init__(self: Self, _value: _T, _prev: Node | None = None, _next: Node | None = None) -> None:
        self.prev: Node
        self.next: Node

    def __setattr__(self: Self, _name: str, _value: Any) -> None:
        if _name == 'next':
            raise AttributeError('cannot assign to field \'next\'')
        object.__setattr__(_name, _value)


class List(MutableSequence[Node[_T]], Generic[_T]):
    'doubly circularly linked list class'
    __slots__ = ('head', )

    @overload
    def __init__(self: Self) -> None: ...
    @overload
    def __init__(self: Self, __i: Iterable[_T]) -> None: ...

    def __init__(self: Self, _iterable: Iterable[_T] | None = None) -> None:
        self.head: Node[None]
        object.__setattr__(self, 'head', Node(None))
        object.__setattr__(self.head, 'next', self.head)
        object.__setattr__(self.head, 'prev', self.head)
        if _iterable is not None:
            for _v in _iterable:
                self.append(_v)

    def __setattr__(self: Self, _name: str, _value: Any) -> None:
        if _name in self.__slots__:
            raise AttributeError('cannot assign to field \'head\' and \'tail\'')
        object.__setattr__(_name, _value)

    def __repr__(self: Self) -> str:
        return repr([v for v in self])

    def __sizeof__(self: Self) -> int:
        return sys.getsizeof(self.head) + sum([sys.getsizeof(_v) for _v in self])

    def __len__(self: Self) -> int:
        _len = 0
        node = self.head.next
        while True:
            if node is self.head:
                break
            node = node.next
            _len += 1
        return _len

    def _valid_index(self: Self, index: int, _raise: bool = True) -> int:
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
    def __getitem__(self: Self, __i: int) -> Node[_T]: ...
    @overload
    def __getitem__(self: Self, __s: slice) -> List[Node[_T]]: ...

    def __getitem__(self: Self, _index: int | slice) -> Node[_T] | List[Node[_T]]:
        if isinstance(_index, int):
            _index = self._valid_index(_index)
            if 0 <= _index:
                node = self.head.next
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index):
                    node = node.next
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            else:
                node = self.head.prev
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(self._valid_index(_index), -1):
                    node = node.prev
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            return node
        elif isinstance(_index, slice):
            start, stop, step = _index.indices(len(self))
            return List([self[_i] for _i in range(start, stop, step)])
        else:
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    @overload
    def __setitem__(self: Self, __i: int, __v: _T) -> None: ...
    @overload
    def __setitem__(self: Self, __s: slice, __o: Iterable[_T]) -> None: ...

    def __setitem__(self: Self, _index: int | slice, _value: _T | Iterable[_T]) -> None:
        if isinstance(_index, int):
            _index = self._valid_index(_index)
            if 0 <= _index:
                node = self.head.next
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index):
                    node = node.next
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            else:
                node = self.head.prev
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index, -1):
                    node = node.prev
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            new_node = Node(_value, node.prev, node.next)
            object.__setattr__(node.prev, 'next', new_node)
            object.__setattr__(node.next, 'prev', new_node)
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
            _index = self._valid_index(_index)
            if 0 <= _index:
                node = self.head.next
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index):
                    node = node.next
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            else:
                node = self.head.prev
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(self._valid_index(_index), -1):
                    node = node.prev
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            object.__setattr__(node.prev, 'next', node.next)
            object.__setattr__(node.next, 'prev', node.prev)
            del node
        elif isinstance(_index, slice):
            start, stop, stride = _index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    def __reversed__(self: Self) -> Iterator[Node[_T]]:
        _i = -1
        try:
            while True:
                _v = self[_i]
                yield _v
                _i -= 1
        except IndexError:
            return

    @overload
    def insert(self: Self, __i: int, __v: _T) -> None: ...
    @overload
    def insert(self: Self, __n: Node[_T], __v: _T) -> None: ...
    @overload
    def insert(self: Self, __n: Node[None], __v: _T) -> None: ...

    def insert(self: Self, _index: int | Node[_T], _value: _T) -> None:
        'insert value to index or next to node'
        try:
            node = Node(_value, _index, _index.next)
            object.__setattr__(_index.next, 'prev', node)
            object.__setattr__(_index, 'next', node)
        except AttributeError as exc:
            if isinstance(_index, int):
                _index = self._valid_index(_index, False)
                if 0 <= _index:
                    node = self.head
                    for _ in range(_index):
                        node = node.next
                        if node is self.head:
                            break
                else:
                    node = self.head
                    for _ in range(_index, 0):
                        node = node.prev
                        if node is self.head:
                            break
                self.insert(node, _value)
            else:
                raise IndexError('index must be integers or a node') from exc

    def append(self: Self, _value: _T) -> None:
        'append value to the end of the sequence'
        node = Node(_value, self.head.prev, self.head)
        object.__setattr__(self.head.prev, 'next', node)
        object.__setattr__(self.head, 'prev', node)

    def reverse(self: Self):
        'reverse the list'
        for i in range(len(self) // 2):
            node_0, node_1 = self[i], self[- (i + 1)]
            prev_0, prev_1 = node_0.prev, node_1.prev
            next_0, next_1 = node_0.next, node_1.next
            object.__setattr__(prev_0, 'next', node_1)
            object.__setattr__(prev_1, 'next', node_0)
            object.__setattr__(node_0, 'next', next_1)
            if next_0 is node_1:
                object.__setattr__(node_1, 'next', node_0)
            else:
                object.__setattr__(node_1, 'next', next_0)
            if node_0 is prev_1:
                object.__setattr__(node_0, 'prev', node_1)
            else:
                object.__setattr__(node_0, 'prev', prev_1)
            object.__setattr__(node_1, 'prev', prev_0)
            if next_0 is node_1:
                object.__setattr__(next_0, 'prev', prev_0)
            else:
                object.__setattr__(next_0, 'prev', node_1)
            object.__setattr__(next_1, 'prev', node_0)

    @overload
    def remove(self: Self, __v: _T) -> None: ...
    @overload
    def remove(self: Self, __n: Node[_T]) -> None: ...

    def remove(self: Self, _value: _T | Node[_T]) -> None:
        'remove first occurrence of value or node'
        try:
            object.__setattr__(_value.prev, 'next', _value.next)
            object.__setattr__(_value.next, 'prev', _value.prev)
            del _value
        except AttributeError:
            del self[self.index(_value)]
