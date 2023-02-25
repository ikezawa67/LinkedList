'''singly circularly linked list module'''
from __future__ import annotations
import sys
import types
from typing import Any, Callable, Generic, TypeVar, Iterable, MutableSequence, overload, Self

_T = TypeVar('_T')


class Node(Generic[_T]):
    '''singly circularly node class'''
    __slots__ = ('value', 'next',)
    value: _T
    next: Node[_T] | Node[None]

    def __new__(cls: type[Self[_T]], _value: _T, _next: Node[_T] | None = None) -> Node[_T]:
        def _is_special(name: str) -> bool:
            if name in {'__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__repr__', '__str__', '__or__', '__ror__'}:
                return True
            elif name in dir(object.__class__):
                return False
            return len(name) > 4 and name[0:2] == name[-2:] == '__'

        def _method(func: Callable):
            def wrapper(*args: Any):
                return func(*tuple(arg.value if hasattr(arg, 'value') else arg for arg in args))
            return wrapper

        classdict = {method: _method(getattr(type(_value), method)) for method in dir(type(_value)) if _is_special(method)}
        classdict.update({'value': _value, 'next': _next})
        _cls = types.new_class('Node', (object, ), exec_body=lambda ns: ns.update(classdict))
        self = object.__new__(_cls)
        self.next = self if _next is None else _next
        return self


class List(MutableSequence[Node[_T]], Generic[_T]):
    'singly circularly linked list class'
    __slots__ = ('head', 'tail', )

    @overload
    def __init__(self: Self[_T]) -> None: ...
    @overload
    def __init__(self: Self[_T], __i: Iterable[_T]) -> None: ...

    def __init__(self: Self[_T], _iterable: Iterable[_T] | None = None) -> None:
        self.head: Node[None] = Node(None)
        self.tail: Node[_T] | Node[None] = self.head
        if isinstance(_iterable, Iterable):
            for _v in _iterable:
                self.append(_v)

    def __repr__(self: Self[_T]) -> str:
        return repr([_v for _v in self])

    def __sizeof__(self: Self[_T]) -> int:
        return sys.getsizeof(self.head) + sum([sys.getsizeof(_v) for _v in self])

    def __len__(self: Self[_T]) -> int:
        _len = 0
        node = self.head.next
        while True:
            if node is self.head:
                break
            node = node.next
            _len += 1
        return _len

    def _valid_index(self: Self[_T], _index: int, _raise: bool = True) -> int:
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
    def __getitem__(self: Self[_T], __i: int) -> Node[_T]: ...
    @overload
    def __getitem__(self: Self[_T], __s: slice) -> Self[_T]: ...

    def __getitem__(self: Self[_T], _index: int | slice) -> Node[_T] | Self[_T]:
        if isinstance(_index, int):
            node = self.head.next
            if node is self.head:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                node = node.next
                if node is self.head:
                    raise IndexError('list assignment index out of range')
            return node
        elif isinstance(_index, slice):
            start, stop, step = _index.indices(len(self))
            return List([self[_i] for _i in range(start, stop, step)])
        else:
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    @overload
    def __setitem__(self: Self[_T], __i: int, __v: _T) -> None: ...
    @overload
    def __setitem__(self: Self[_T], __s: slice, __o: Iterable[_T]) -> None: ...

    def __setitem__(self: Self[_T], _index: int | slice, _value: _T | Iterable[_T]) -> None:
        if isinstance(_index, int):
            prev = self.head
            node = prev.next
            if node is self.head:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                prev = node
                node = prev.next
                if node is self.head:
                    raise IndexError('list assignment index out of range')
            prev.value = _value
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
    def __delitem__(self: Self[_T], __i: int) -> None: ...
    @overload
    def __delitem__(self: Self[_T], __s: slice) -> None: ...

    def __delitem__(self: Self[_T], _index: int | slice) -> None:
        if isinstance(_index, int):
            prev = self.head
            node = prev.next
            if node is self.head:
                raise IndexError('list assignment index out of range')
            for _ in range(self._valid_index(_index)):
                prev = node
                node = prev.next
                if node is self.head:
                    raise IndexError('list assignment index out of range')
            prev.next = node.next
            if prev.next is self.head:
                self.tail = self.head
            del node
        elif isinstance(_index, slice):
            start, stop, stride = _index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    @overload
    def insert(self: Self[_T], __i: int, __v: _T) -> None: ...
    @overload
    def insert(self: Self[_T], __n: Node[_T], __v: _T) -> None: ...
    @overload
    def insert(self: Self[_T], __n: Node[None], __v: _T) -> None: ...

    def insert(self: Self[_T], _index: int | Node[_T] | Node[None], _value: _T) -> None:
        'insert value to index or next to node'
        try:
            node = Node(_value, _index.next)
            if node.next is self.head:
                self.tail= node
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

    def append(self, _value: _T) -> None:
        'append value to the end of the sequence'
        self.insert(self.tail, _value)

    def reverse(self: Self[_T]):
        'reverse the list'
        _n = len(self)
        for i in range(_n // 2):
            prev_0, prev_1 = self.head if i == 0 else self[i - 1], self[_n - i - 2]
            node_0, node_1 = prev_0.next, prev_1.next
            next_0, next_1 = node_0.next, node_1.next
            prev_0.next = node_1
            prev_1.next = node_0
            node_0.next = next_1
            if next_0 is node_1:
                node_1.next = node_0
            else:
                node_1.next = next_0
            if node_1 is self.tail:
                self.tail = node_0
