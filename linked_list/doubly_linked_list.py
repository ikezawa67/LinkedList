'''doubly linked list module'''
from __future__ import annotations
import sys
import types
from typing import Any, Callable, Generic, TypeVar, Iterable, Iterator, MutableSequence, overload, Self

_T = TypeVar('_T')


class Node(Generic[_T]):
    'doubly linked node class'
    __slots__ = ('value', '_prev', '_next',)
    value: _T
    prev: Node[_T] | Node[None] | None
    next: Node[_T] | Node[None] | None

    def __new__(cls: type[Self[_T]], _value: _T, _prev: Node[_T] | Node[None] | None = None, _next: Node[_T] | Node[None] | None = None) -> Node[_T]:
        def _is_sunder(name: str) -> bool:
            if name in {'__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__repr__', '__str__', '__or__', '__ror__'}:
                return True
            elif name in dir(object.__class__):
                return False
            return len(name) > 4 and name[0:2] == name[-2:] == '__'

        def _method(func: Callable):
            def wrapper(*args: Any):
                self = args[0].value
                if 1 == len(args):
                    return func(self)
                else:
                    return func(self, *args[1:])
            return wrapper
        
        classdict = {method: _method(getattr(type(_value), method)) for method in dir(type(_value)) if _is_sunder(method)}
        classdict.update({'value': _value, 'prev':Node.prev , 'next': Node.next})
        _cls = types.new_class('Node', (object, ), exec_body=lambda ns: ns.update(classdict))
        self = object.__new__(_cls)
        self.prev = _prev
        self.next = _next
        return self

    @property
    def prev(self) -> Node[_T] | Node[None] | None:
        '''prev node'''
        return self._prev

    @prev.setter
    def prev(self, _prev: Node[_T] | Node[None]) -> None:
        self._prev = _prev
        if hasattr(_prev, 'next') and _prev.next is not self:
            _prev.next = self

    @property
    def next(self) -> Node[_T] | Node[None] | None:
        '''next node'''
        return self._next

    @next.setter
    def next(self, _next: Node[_T] | Node[None]) -> None:
        self._next = _next
        if hasattr(_next, 'prev') and _next.prev is not self:
            _next.prev = self


class List(MutableSequence[Node[_T]], Generic[_T]):
    'doubly linked list class'
    __slots__ = ('head', 'tail', )

    @overload
    def __init__(self: Self[_T]) -> None: ...
    @overload
    def __init__(self: Self[_T], __i: Iterable[_T]) -> None: ...

    def __init__(self: Self[_T], _iterable: Iterable[_T] | None = None) -> None:
        self.head: Node[None] = Node(None)
        self.tail: Node[None] = Node(None, self.head)
        if isinstance(_iterable, Iterable):
            for _v in _iterable:
                self.append(_v)

    def __repr__(self: Self[_T]) -> str:
        return repr([_v for _v in self])

    def __sizeof__(self: Self[_T]) -> int:
        return sys.getsizeof(self.head) + sum([sys.getsizeof(_v) for _v in self]) + sys.getsizeof(self.tail)

    def __len__(self: Self[_T]) -> int:
        _len = 0
        node = self.head.next
        while True:
            if node is self.tail:
                break
            node = node.next
            _len += 1
        return _len

    def _valid_index(self: Self[_T], _index: int, _raise: bool = True) -> int:
        _n = len(self)
        if 0 <= _index:
            if _index > _n:
                if _raise:
                    raise IndexError('list assignment index out of range')
                _index = _n
        else:
            if abs(_index) > _n + 1:
                if _raise:
                    raise IndexError('list assignment index out of range')
                _index = - (_n + 1)
        return _index

    @overload
    def __getitem__(self: Self[_T], __i: int) -> Node[_T]: ...
    @overload
    def __getitem__(self: Self[_T], __s: slice) -> Self[_T]: ...

    def __getitem__(self: Self[_T], _index: int | slice) -> Node[_T] | Self[_T]:
        if isinstance(_index, int):
            _index = self._valid_index(_index)
            if 0 <= _index:
                node = self.head.next
                if node is self.tail:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index):
                    node = node.next
                    if node is self.tail:
                        raise IndexError('list assignment index out of range')
            else:
                node = self.tail.prev
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
    def __setitem__(self: Self[_T], __i: int, __v: _T) -> None: ...
    @overload
    def __setitem__(self: Self[_T], __s: slice, __o: Iterable[_T]) -> None: ...

    def __setitem__(self: Self[_T], _index: int | slice, _value: _T | Iterable[_T]) -> None:
        if isinstance(_index, int):
            _index = self._valid_index(_index)
            if 0 <= _index:
                node = self.head.next
                if node is self.tail:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index):
                    node = node.next
                    if node is self.tail:
                        raise IndexError('list assignment index out of range')
            else:
                node = self.tail.prev
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index, -1):
                    node = node.prev
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            node.value = _value
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
            _index = self._valid_index(_index)
            if 0 <= _index:
                node = self.head.next
                if node is self.tail:
                    raise IndexError('list assignment index out of range')
                for _ in range(_index):
                    node = node.next
                    if node is self.tail:
                        raise IndexError('list assignment index out of range')
            else:
                node = self.tail.prev
                if node is self.head:
                    raise IndexError('list assignment index out of range')
                for _ in range(self._valid_index(_index), -1):
                    node = node.prev
                    if node is self.head:
                        raise IndexError('list assignment index out of range')
            node.prev.next = node.next
            del node
        elif isinstance(_index, slice):
            start, stop, stride = _index.indices(len(self))
            for _i in range(start, stop, stride):
                del self[_i]
        else:
            raise TypeError(f'index must be integers or slices, not {type(_index)}')

    def __reversed__(self: Self[_T]) -> Iterator[Node[_T]]:
        _i = -1
        try:
            while True:
                _v = self[_i]
                yield _v
                _i -= 1
        except IndexError:
            return

    @overload
    def insert(self: Self[_T], __i: int, __v: _T) -> None: ...
    @overload
    def insert(self: Self[_T], __n: Node[_T], __v: _T) -> None: ...
    @overload
    def insert(self: Self[_T], __n: Node[None], __v: _T) -> None: ...

    def insert(self: Self[_T], _index: int | Node[_T] | Node[None], _value: _T) -> None:
        'insert value to index or next to node'
        try:
            if _index is self.tail:
                raise IndexError('cannot insert next to tail node')
            Node(_value, _index, _index.next)
        except AttributeError as exc:
            if isinstance(_index, int):
                _index = self._valid_index(_index, False)
                if 0 <= _index:
                    node = self.head
                    for _ in range(_index):
                        if node is self.tail:
                            break
                        node = node.next
                else:
                    node = self.tail
                    for _ in range(_index, 0):
                        if node is self.head:
                            break
                        node = node.prev
                self.insert(node, _value)
            else:
                raise IndexError('index must be integers or a node') from exc

    def append(self: Self[_T], _value: _T) -> None:
        'append value to the end of the sequence'
        self.insert(self.tail.prev, _value)

    def reverse(self: Self[_T]):
        'reverse the list'
        for i in range(len(self) // 2):
            node_0, node_1 = self[i], self[- (i + 1)]
            prev_0, prev_1 = node_0.prev, node_1.prev
            next_0, next_1 = node_0.next, node_1.next
            prev_0.next = node_1
            prev_1.next = node_0
            node_0.next = next_1
            if next_0 is node_1:
                node_1.next = node_0
            else:
                node_1.next = next_0
            if node_0 is prev_1:
                node_0.prev = node_1
            else:
                node_0.prev = prev_1
            node_1.prev = prev_0
            if next_0 is node_1:
                next_0.prev = prev_0
            else:
                next_0.prev = node_1
            next_1.prev = node_0

    @overload
    def remove(self: Self[_T], __v: _T) -> None: ...
    @overload
    def remove(self: Self[_T], __n: Node[_T]) -> None: ...

    def remove(self: Self[_T], _value: _T | Node[_T]) -> None:
        'remove first occurrence of value or node'
        try:
            _value.prev.next = _value.next
            del _value
        except AttributeError:
            del self[self.index(_value)]
