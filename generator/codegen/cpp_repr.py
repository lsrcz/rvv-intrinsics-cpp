from typing import Protocol, Union


class HasCppReprProperty(Protocol):
    @property
    def cpp_repr(self) -> str:
        raise NotImplementedError


HasCppRepr = Union[str, HasCppReprProperty]


def to_cpp_repr(x: HasCppRepr) -> str:
    if isinstance(x, str):
        return x
    return x.cpp_repr
