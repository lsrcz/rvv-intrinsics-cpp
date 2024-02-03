from . import type
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class PtrType(type.Type):
    base_type: type.Type
    is_const: bool

    @property
    def cpp_repr(self) -> str:
        if isinstance(self.base_type, PtrType):
            raise ValueError("Nested pointers are not supported and not needed")
        quantifier: str = f"{'const ' if self.is_const else ''}"
        return f"{quantifier}{self.base_type.cpp_repr} *"


@dataclass(frozen=True, kw_only=True)
class VoidType(type.Type):
    @property
    def cpp_repr(self) -> str:
        return "void"


@dataclass(frozen=True, kw_only=True)
class SizeTType(type.Type):
    @property
    def cpp_repr(self) -> str:
        return "size_t"


size_t_kind: type.DataKind = type.DataKind(data_type=SizeTType())


@dataclass(frozen=True, kw_only=True)
class SizeTValue(type.Type):
    pass


@dataclass(frozen=True, kw_only=True)
class LitSizeTValue(SizeTValue):
    value: int

    @property
    def cpp_repr(self) -> str:
        return str(self.value)


@dataclass(frozen=True, kw_only=True)
class ParamSizeTValue(SizeTValue, type.TypeParam):
    @property
    def kind(self) -> type.DataKind:
        return size_t_kind


@dataclass(frozen=True, kw_only=True)
class PtrdiffTType(type.Type):
    @property
    def cpp_repr(self) -> str:
        return "ptrdiff_t"
