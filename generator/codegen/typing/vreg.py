import abc
from dataclasses import dataclass

from codegen.typing import base, elem
from codegen.typing import kind as k
from codegen.typing import misc


@dataclass(frozen=True, kw_only=True)
class VRegType(base.Type, metaclass=abc.ABCMeta):
    pass


@dataclass(frozen=True, kw_only=True)
class ConcreteVRegType(VRegType):
    elem_type: elem.ElemType
    ratio: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vreg_t<{self.elem_type.cpp_repr}, {self.ratio.cpp_repr}>"


def concrete(
    elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> ConcreteVRegType:
    return ConcreteVRegType(elem_type=elem_type, ratio=ratio)


@dataclass(frozen=True, kw_only=True)
class RawVRegType(ConcreteVRegType):
    elem_type: elem.RawElemType
    ratio: misc.LitSizeTValue


def raw(elem_type: elem.RawElemType, ratio: misc.LitSizeTValue) -> RawVRegType:
    return RawVRegType(elem_type=elem_type, ratio=ratio)


@dataclass(frozen=True, kw_only=True)
class ParamVRegType(VRegType, base.TypeParam):
    @property
    def kind(self) -> k.TypeKind:
        return k.type_kind


def param(typename: str) -> ParamVRegType:
    return ParamVRegType(typename=typename)


@dataclass(frozen=True, kw_only=True)
class WidenVRegType(VRegType):
    base_type: VRegType

    @property
    def cpp_repr(self) -> str:
        return f"widen_t<{self.base_type.cpp_repr}>"


def widen(vreg_type: VRegType) -> WidenVRegType:
    return WidenVRegType(base_type=vreg_type)


@dataclass(frozen=True, kw_only=True)
class NarrowVRegType(VRegType):
    base_type: VRegType

    @property
    def cpp_repr(self) -> str:
        return f"narrow_t<{self.base_type.cpp_repr}>"


def narrow(vreg_type: VRegType) -> NarrowVRegType:
    return NarrowVRegType(base_type=vreg_type)


@dataclass(frozen=True, kw_only=True)
class WidenNVRegType(VRegType):
    n: int
    base_type: VRegType

    @property
    def cpp_repr(self) -> str:
        return f"widen_n_t<{self.n}, {self.base_type.cpp_repr}>"


def widen_n(n: int, vreg_type: VRegType) -> WidenNVRegType:
    return WidenNVRegType(n=n, base_type=vreg_type)


@dataclass(frozen=True, kw_only=True)
class ToUnsignedVRegType(VRegType):
    base_type: VRegType

    @property
    def cpp_repr(self) -> str:
        return f"to_unsigned_t<{self.base_type.cpp_repr}>"


def to_unsigned(vreg_type: VRegType) -> ToUnsignedVRegType:
    return ToUnsignedVRegType(base_type=vreg_type)
