'''linked list utility module'''
from typing import Any, Self


class _Protect:
    __protect__: tuple[str] = ('__protect__', )

    def __setattr__(self: Self, _name: str, _value: Any) -> None:
        if _name in self.__protect__:
            raise AttributeError(f'cannot assign to field \'{_name}\'')
        elif not (len(_name) > 4 and _name[:2] == _name[-2:] == '__' and _name[2] != '_' and _name[-3] != '_'):
            object.__setattr__(self, '__protect__', self.__protect__ + (_name, ))
        object.__setattr__(self, _name, _value)

    def __delattr__(self, _name: str) -> None:
        if _name in self.__protect__:
            raise AttributeError(f'cannot assign to field \'{_name}\'')
        object.__delattr__(self, _name)
