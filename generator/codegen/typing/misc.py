import abc
from dataclasses import dataclass

from codegen.typing import base


@dataclass(frozen=True, kw_only=True)
class PtrType(base.Type):
    base_type: base.Type
    is_const: bool

    @property
    def cpp_repr(self) -> str:
        if isinstance(self.base_type, PtrType):
            raise ValueError("Nested pointers are not supported and not needed")
        quantifier: str = f"{'const ' if self.is_const else ''}"
        return f"{quantifier}{self.base_type.cpp_repr} *"


def ptr(base_type: base.Type, *, is_const: bool) -> PtrType:
    return PtrType(base_type=base_type, is_const=is_const)


@dataclass(frozen=True, kw_only=True)
class VoidType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "void"


void = VoidType()


@dataclass(frozen=True, kw_only=True)
class SizeTType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "size_t"


size_t = SizeTType()


size_t_kind: base.DataKind = base.DataKind(data_type=SizeTType())


@dataclass(frozen=True, kw_only=True)
class SizeTValue(base.Type, metaclass=abc.ABCMeta):
    pass


@dataclass(frozen=True, kw_only=True)
class LitSizeTValue(SizeTValue):
    value: int

    @property
    def cpp_repr(self) -> str:
        return str(self.value)


ALL_TUPLE_SIZE: list[LitSizeTValue] = [
    LitSizeTValue(value=2),
    LitSizeTValue(value=3),
    LitSizeTValue(value=4),
    LitSizeTValue(value=5),
    LitSizeTValue(value=6),
    LitSizeTValue(value=7),
    LitSizeTValue(value=8),
]

ALL_INDEX: list[LitSizeTValue] = [
    LitSizeTValue(value=0),
    LitSizeTValue(value=1),
    LitSizeTValue(value=2),
    LitSizeTValue(value=3),
    LitSizeTValue(value=4),
    LitSizeTValue(value=5),
    LitSizeTValue(value=6),
    LitSizeTValue(value=7),
]


def lit_size_t(value: int) -> LitSizeTValue:
    return LitSizeTValue(value=value)


ALL_RATIO: list[LitSizeTValue] = [
    LitSizeTValue(value=1),
    LitSizeTValue(value=2),
    LitSizeTValue(value=4),
    LitSizeTValue(value=8),
    LitSizeTValue(value=16),
    LitSizeTValue(value=32),
    LitSizeTValue(value=64),
]


@dataclass(frozen=True, kw_only=True)
class ParamSizeTValue(SizeTValue, base.TypeParam):
    @property
    def kind(self) -> base.DataKind:
        return size_t_kind


def param_size_t(typename: str) -> ParamSizeTValue:
    return ParamSizeTValue(typename=typename)


@dataclass(frozen=True, kw_only=True)
class PtrdiffTType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "ptrdiff_t"


ptrdiff_t = PtrdiffTType()


@dataclass(frozen=True, kw_only=True)
class VXRMType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "VXRM"


vxrm = VXRMType()


@dataclass(frozen=True, kw_only=True)
class ParamVXRMValue(base.TypeParam, base.Type):
    @property
    def kind(self) -> base.DataKind:
        return base.DataKind(data_type=VXRMType())

    @property
    def cpp_repr(self) -> str:
        return self.typename


def param_vxrm(typename: str) -> ParamVXRMValue:
    return ParamVXRMValue(typename=typename)


@dataclass(frozen=True, kw_only=True)
class FRMType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "FRM"


frm = FRMType()


@dataclass(frozen=True, kw_only=True)
class ParamFRMValue(base.TypeParam, base.Type):
    @property
    def kind(self) -> base.DataKind:
        return base.DataKind(data_type=FRMType())

    @property
    def cpp_repr(self) -> str:
        return self.typename


def param_frm(typename: str) -> ParamFRMValue:
    return ParamFRMValue(typename=typename)


@dataclass(frozen=True, kw_only=True)
class CUnsignedIntType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "unsigned int"


c_unsigned_int_t = CUnsignedIntType()


@dataclass(frozen=True, kw_only=True)
class CIntType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "int"


c_int_t = CIntType()
