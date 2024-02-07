import abc
from dataclasses import dataclass

from codegen.typing import kind as k


@dataclass(frozen=True, kw_only=True)
class Type(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def cpp_repr(self) -> str:
        pass

    def __str__(self) -> str:
        return self.cpp_repr


@dataclass(frozen=True, kw_only=True)
class DataKind(k.Kind):
    data_type: Type

    @property
    def cpp_repr(self) -> str:
        return self.data_type.cpp_repr


@dataclass(frozen=True, kw_only=True)
class TypeParam(Type):
    typename: str

    @property
    def cpp_repr(self) -> str:
        return self.typename

    @property
    @abc.abstractmethod
    def kind(self) -> k.Kind:
        pass
