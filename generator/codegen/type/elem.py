import abc
from typing import Sequence
from . import type
from . import kind as k
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ElemType(type.Type):
    pass


@dataclass(frozen=True, kw_only=True)
class RawElemType(ElemType):
    @property
    @abc.abstractmethod
    def long_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def short_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def element_width(self) -> int:
        pass

    @property
    def cpp_repr(self) -> str:
        return f"{self.long_name}_t"


@dataclass(frozen=True, kw_only=True)
class IntType(RawElemType):
    width: int
    signed: bool

    def __post_init__(self) -> None:
        assert self.width in [8, 16, 32, 64]

    @property
    def long_name(self) -> str:
        return f"{'' if self.signed else 'u'}int{self.width}"

    @property
    def short_name(self) -> str:
        return f"{'i' if self.signed else 'u'}{self.width}"

    @property
    def element_width(self) -> int:
        return self.width


@dataclass(frozen=True, kw_only=True)
class FloatType(RawElemType):
    width: int

    def __post_init__(self) -> None:
        assert self.width in [16, 32, 64]

    @property
    def long_name(self) -> str:
        return f"float{self.width}"

    @property
    def short_name(self) -> str:
        return f"f{self.width}"

    @property
    def element_width(self) -> int:
        return self.width


ALL_UNSIGNED_INT_TYPES: list[IntType] = [
    IntType(width=8, signed=False),
    IntType(width=16, signed=False),
    IntType(width=32, signed=False),
    IntType(width=64, signed=False),
]

ALL_SIGNED_INT_TYPES: list[IntType] = [
    IntType(width=8, signed=True),
    IntType(width=16, signed=True),
    IntType(width=32, signed=True),
    IntType(width=64, signed=True),
]

ALL_INT_TYPES: list[IntType] = ALL_UNSIGNED_INT_TYPES + ALL_SIGNED_INT_TYPES

ALL_FLOAT_TYPES: list[FloatType] = [
    FloatType(width=16),
    FloatType(width=32),
    FloatType(width=64),
]

ALL_ELEM_TYPES: Sequence[RawElemType] = ALL_INT_TYPES + ALL_FLOAT_TYPES


@dataclass(frozen=True, kw_only=True)
class ParamElemType(ElemType, type.TypeParam):
    @property
    def kind(self) -> k.TypeKind:
        return k.TypeKind()
