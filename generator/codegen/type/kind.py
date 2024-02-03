import abc
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Kind(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def cpp_repr(self) -> str:
        pass


@dataclass(frozen=True, kw_only=True)
class TypeKind(Kind):
    @property
    def cpp_repr(self) -> str:
        return "typename"
