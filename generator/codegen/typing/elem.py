import abc
from dataclasses import dataclass
from typing import Sequence

from codegen.typing import base
from codegen.typing import kind as k


@dataclass(frozen=True, kw_only=True)
class ElemType(base.Type, metaclass=abc.ABCMeta):
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


def int_type(width: int, signed: bool) -> IntType:
    return IntType(width=width, signed=signed)


def signed_type(width: int) -> IntType:
    return int_type(width=width, signed=True)


def unsigned_type(width: int) -> IntType:
    return int_type(width=width, signed=False)


int8_t = signed_type(8)
int16_t = signed_type(16)
int32_t = signed_type(32)
int64_t = signed_type(64)
uint8_t = unsigned_type(8)
uint16_t = unsigned_type(16)
uint32_t = unsigned_type(32)
uint64_t = unsigned_type(64)


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


def float_type(width: int) -> FloatType:
    return FloatType(width=width)


float16_t = float_type(16)
float32_t = float_type(32)
float64_t = float_type(64)


ALL_UNSIGNED_INT_TYPES: list[IntType] = [uint8_t, uint16_t, uint32_t, uint64_t]

ALL_SIGNED_INT_TYPES: list[IntType] = [int8_t, int16_t, int32_t, int64_t]

ALL_INT_TYPES: list[IntType] = ALL_UNSIGNED_INT_TYPES + ALL_SIGNED_INT_TYPES

ALL_FLOAT_TYPES: list[FloatType] = [float16_t, float32_t, float64_t]

ALL_ELEM_TYPES: Sequence[RawElemType] = ALL_INT_TYPES + ALL_FLOAT_TYPES

ALL_ELEM_SIZES: list[int] = [8, 16, 32, 64]


@dataclass(frozen=True, kw_only=True)
class ParamElemType(ElemType, base.TypeParam):
    @property
    def kind(self) -> k.TypeKind:
        return k.type_kind


def param(typename: str) -> ParamElemType:
    return ParamElemType(typename=typename)


@dataclass(frozen=True, kw_only=True)
class WidenElemType(ElemType):
    base_type: ElemType

    @property
    def cpp_repr(self) -> str:
        return f"widen_t<{self.base_type.cpp_repr}>"


def widen(elem_type: ElemType) -> WidenElemType:
    return WidenElemType(base_type=elem_type)
